#include <Os/FileSystem.hpp>
#include <Os/File.hpp>
#include <Fw/Types/Assert.hpp>

#include <zephyr/fs/fs.h>
#include <zephyr/kernel.h>
#include <errno.h>


// #define DEBUG_PRINT(x,...) printk(x,##__VA_ARGS__);
#define DEBUG_PRINT(x,...)

namespace Os {
namespace FileSystem {

// Helpers in anonymous namespace.
namespace {

Status handleFileError(File::Status fileStatus) {
    Status fileSystemStatus = OTHER_ERROR;

    switch (fileStatus) {
        case File::NO_SPACE:
            fileSystemStatus = NO_SPACE;
            break;
        case File::NO_PERMISSION:
            fileSystemStatus = NO_PERMISSION;
            break;
        case File::DOESNT_EXIST:
            fileSystemStatus = INVALID_PATH;
            break;
        default:
            fileSystemStatus = OTHER_ERROR;
    }
    return fileSystemStatus;
}

/**
 * A helper function that writes all the file information in the source
 * file to the destination file (replaces/appends to end/etc. depending
 * on destination file mode).
 *
 * Files must already be open and will remain open after this function
 * completes.
 *
 * @param source File to copy data from
 * @param destination File to copy data to
 * @param size The number of bytes to copy
 */
Status copyFileData(File source, File destination, FwSizeType size) {
    static_assert(FILE_SYSTEM_CHUNK_SIZE != 0, "FILE_SYSTEM_CHUNK_SIZE must be >0");
    U8 fileBuffer[FILE_SYSTEM_CHUNK_SIZE];
    File::Status file_status;

    // Set loop limit
    const FwSizeType copyLoopLimit = (size / FILE_SYSTEM_CHUNK_SIZE) + 2;

    FwSizeType loopCounter = 0;
    NATIVE_INT_TYPE chunkSize;
    while (loopCounter < copyLoopLimit) {
        chunkSize = FILE_SYSTEM_CHUNK_SIZE;
        file_status = source.read(fileBuffer, chunkSize, false);
        if (file_status != File::OP_OK) {
            return handleFileError(file_status);
        }

        if (chunkSize == 0) {
            // file has been successfully copied
            break;
        }

        file_status = destination.write(fileBuffer, chunkSize, true);
        if (file_status != File::OP_OK) {
            return handleFileError(file_status);
        }
        loopCounter++;
    }
    FW_ASSERT(loopCounter < copyLoopLimit);

    return FileSystem::OP_OK;
}

}  // end anonymous namespace

Status createDirectory(const char* path) {
    int ret = fs_mkdir(path);

    if (ret == -EEXIST) {
        return Status::ALREADY_EXISTS;
    } else if (ret < 0) {
        return Status::OTHER_ERROR;
    }
    
    return Status::OP_OK;
}

Status removeDirectory(const char* path) {
    return removeFile(path);
}

Status removeFile(const char* path) {
    int ret = fs_unlink(path);
    if (ret == -EINVAL) {
        return Status::INVALID_PATH;
    } else if (ret < 0) {
        return Status::OTHER_ERROR;
    }

    return Status::OP_OK;
}

Status moveFile(const char* originPath, const char* destPath) {
    int ret = fs_rename(originPath, destPath);
    if (ret == -EINVAL) {
        return Status::INVALID_PATH;
    } else if (ret < 0) {
        return Status::OTHER_ERROR;
    }

    return Status::OP_OK;
}

Status copyFile(const char* originPath, const char* destPath) {
    // Remove destination file if it exists.
    int ret = fs_unlink(destPath);
    if (ret != 0 || ret != -EINVAL) {
        return Status::OTHER_ERROR;
    }

    // Destination file now doesn't exist so we can use appendFile().
    return appendFile(originPath, destPath, /*createMissingDest=*/true);
}

Status appendFile(const char* originPath, const char* destPath, bool createMissingDest) {
    FileSystem::Status fs_status;
    File::Status file_status;
    FwSizeType fileSize = 0;

    File source;
    File destination;

    // Get the file size:
    fs_status =
        FileSystem::getFileSize(originPath, fileSize);  //!< gets the size of the file (in bytes) at location path
    if (FileSystem::OP_OK != fs_status) {
        return fs_status;
    }

    // If needed, check if destination file exists (and exit if not)
    if (!createMissingDest) {
        FwSizeType size;
        fs_status = getFileSize(destPath, size);
        if (FileSystem::OP_OK != fs_status) {
            return fs_status;
        }
    }

    file_status = source.open(originPath, File::OPEN_READ);
    if (file_status != File::OP_OK) {
        return handleFileError(file_status);
    }


    file_status = destination.open(destPath, File::OPEN_APPEND);
    if (file_status != File::OP_OK) {
        return handleFileError(file_status);
    }

    fs_status = copyFileData(source, destination, fileSize);
    (void)source.close();
    (void)destination.close();
    return fs_status;
}

Status getFileSize(const char* path, FwSizeType& size) {
    struct fs_dirent entry;
    int ret = fs_stat(path, &entry);
    if (ret == -EINVAL || ret == -ENOENT) {
        return Status::INVALID_PATH;
    } else if (ret < 0) {
        return Status::OTHER_ERROR;
    }

    size = entry.size;
    return Status::OP_OK;
}

}   // end namespace FileSystem
}   // end namespace Os