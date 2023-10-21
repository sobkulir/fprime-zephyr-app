import os
import subprocess
from string import Template
import shutil

TMPL = 'tmpl'
TARGET = 'target'

F_PRIME_PATH = '/zephyr-workspace/fprime-zephyr-app/fprime'
LED_BLINKER_PATH = '/zephyr-workspace/fprime-zephyr-app/LedBlinker'
BENCH_PATH = os.path.join(LED_BLINKER_PATH, 'bench')
BACKUP_PATH = os.path.join(BENCH_PATH, 'backups')
REPORT_PATH = os.path.join(BENCH_PATH, 'report')
TMPL_PATH = os.path.join(BENCH_PATH, 'tmpl')

# All files to template
AC_CONSTANTS_FPP = 'AcConstants.fpp'
FP_CONFIG_H = 'FpConfig.h'
STATIC_MEMORY_CONFIG_HPP = 'StaticMemoryConfig.hpp'
TLM_CHAN_IMPL_CFG_HPP = 'TlmChanImplCfg.hpp'
PRJ_CONF = 'prj.conf'
SETTINGS_INI = 'settings.ini'
INSTANCES_FPP = 'instances.fpp'
TOPOLOGY_FPP = 'topology.fpp'
LOG_ASSERT_HPP = 'LogAssert.hpp'
FPRIME_SVC_CMAKELISTS_TXT = 'FprimeSvcCMakeLists.txt'
FPRIME_FW_CMAKELISTS_TXT = 'FprimeFwCMakeLists.txt'

TEMPLATES = {
    AC_CONSTANTS_FPP: {
        TMPL: os.path.join(TMPL_PATH, AC_CONSTANTS_FPP + '.tmpl'),
        TARGET: os.path.join(LED_BLINKER_PATH, 'config', AC_CONSTANTS_FPP),
    },
    FP_CONFIG_H: {
        TMPL: os.path.join(TMPL_PATH, FP_CONFIG_H + '.tmpl'),
        TARGET: os.path.join(LED_BLINKER_PATH, 'config', FP_CONFIG_H),
    },
    STATIC_MEMORY_CONFIG_HPP: {
        TMPL: os.path.join(TMPL_PATH, STATIC_MEMORY_CONFIG_HPP + '.tmpl'),
        TARGET: os.path.join(LED_BLINKER_PATH, 'config', STATIC_MEMORY_CONFIG_HPP),
    },
    TLM_CHAN_IMPL_CFG_HPP: {
        TMPL: os.path.join(TMPL_PATH, TLM_CHAN_IMPL_CFG_HPP + '.tmpl'),
        TARGET: os.path.join(LED_BLINKER_PATH, 'config', TLM_CHAN_IMPL_CFG_HPP),
    },
    PRJ_CONF: {
        TMPL: os.path.join(TMPL_PATH, PRJ_CONF + '.tmpl'),
        TARGET: os.path.join(LED_BLINKER_PATH, PRJ_CONF),
    },
    SETTINGS_INI: {
        TMPL: os.path.join(TMPL_PATH, SETTINGS_INI + '.tmpl'),
        TARGET: os.path.join(LED_BLINKER_PATH, SETTINGS_INI),
    },
    INSTANCES_FPP: {
        TMPL: os.path.join(TMPL_PATH, INSTANCES_FPP + '.tmpl'),
        TARGET: os.path.join(LED_BLINKER_PATH, 'Top', INSTANCES_FPP),
    },
    TOPOLOGY_FPP: {
        TMPL: os.path.join(TMPL_PATH, TOPOLOGY_FPP + '.tmpl'),
        TARGET: os.path.join(LED_BLINKER_PATH, 'Top', TOPOLOGY_FPP),
    },

    # F Prime patches to compile without assertions and without event logging.
    LOG_ASSERT_HPP: {
        TMPL: os.path.join(TMPL_PATH, LOG_ASSERT_HPP + '.tmpl'),
        TARGET: os.path.join(F_PRIME_PATH, 'Fw', 'Logger', LOG_ASSERT_HPP),
    },
    FPRIME_SVC_CMAKELISTS_TXT: {
        TMPL: os.path.join(TMPL_PATH, FPRIME_SVC_CMAKELISTS_TXT + '.tmpl'),
        TARGET: os.path.join(F_PRIME_PATH, 'Svc', 'CMakeLists.txt'),
    },
    FPRIME_FW_CMAKELISTS_TXT: {
        TMPL: os.path.join(TMPL_PATH, FPRIME_FW_CMAKELISTS_TXT + '.tmpl'),
        TARGET: os.path.join(F_PRIME_PATH, 'Fw', 'CMakeLists.txt'),
    },
}

# Define the replacement values
BASE = {
    'tag': 'base',

    AC_CONSTANTS_FPP: {
        'PassiveRateGroupOutputPorts': '10',
        'CmdDispatcherComponentCommandPorts': '30',
        'StaticMemoryAllocations': '4',
    },
    FP_CONFIG_H: {
        'FW_OBJECT_NAMES': '1',
        'FW_OBJECT_REGISTRATION': '1',
        'FW_PORT_TRACING': '1',
        'FW_ENABLE_TEXT_LOGGING': '1',
        'FW_PORT_SERIALIZATION': '1',
        'FW_ASSERT_LEVEL': 'FW_FILENAME_ASSERT',
    },
    STATIC_MEMORY_CONFIG_HPP: {
        'STATIC_MEMORY_ALLOCATION_SIZE': 2048,
    },
    TLM_CHAN_IMPL_CFG_HPP: {
        'TLMCHAN_HASH_BUCKETS': 50,
    },
    PRJ_CONF: {
        'CONFIG_HEAP_MEM_POOL_SIZE': 60000,
    },
    INSTANCES_FPP: {
        'COMMENT_OUT_TEXT_LOGGER': '',
    },
    TOPOLOGY_FPP: {
        'COMMENT_OUT_TEXT_LOGGER': '',
    },
    SETTINGS_INI: {
        'FPRIME_ENABLE_TEXT_LOGGERS': 'ON',
    },
    LOG_ASSERT_HPP: None,
    FPRIME_SVC_CMAKELISTS_TXT: None,
    FPRIME_FW_CMAKELISTS_TXT: None,
}

BASE_REG = {
    **BASE,
    **{
        'tag': 'base,reg',

        FP_CONFIG_H: {
            'FW_OBJECT_NAMES': '1',
            'FW_OBJECT_REGISTRATION': '0',
            'FW_PORT_TRACING': '1',
            'FW_ENABLE_TEXT_LOGGING': '1',
            'FW_PORT_SERIALIZATION': '1',
            'FW_ASSERT_LEVEL': 'FW_FILENAME_ASSERT',
        },
    }
}

BASE_REG_TRC = {
    **BASE,
    **{
        'tag': 'base,reg,trc',

        FP_CONFIG_H: {
            'FW_OBJECT_NAMES': '1',
            'FW_OBJECT_REGISTRATION': '0',
            'FW_PORT_TRACING': '0',
            'FW_ENABLE_TEXT_LOGGING': '1',
            'FW_PORT_SERIALIZATION': '1',
            'FW_ASSERT_LEVEL': 'FW_FILENAME_ASSERT',
        },
    }
}

BASE_REG_TRC_SER = {
    **BASE,
    **{
        'tag': 'base,reg,trc,ser',

        FP_CONFIG_H: {
            'FW_OBJECT_NAMES': '1',
            'FW_OBJECT_REGISTRATION': '0',
            'FW_PORT_TRACING': '0',
            'FW_ENABLE_TEXT_LOGGING': '1',
            'FW_PORT_SERIALIZATION': '0',
            'FW_ASSERT_LEVEL': 'FW_FILENAME_ASSERT',
        },
    }
}

BASE_REG_TRC_SER_RTGR = {
    **BASE,
    **{
        'tag': 'base,reg,trc,ser,rtgr',
        AC_CONSTANTS_FPP: {
            'PassiveRateGroupOutputPorts': '4',
            'CmdDispatcherComponentCommandPorts': '30',
            'StaticMemoryAllocations': '4',
        },

        FP_CONFIG_H: {
            'FW_OBJECT_NAMES': '1',
            'FW_OBJECT_REGISTRATION': '0',
            'FW_PORT_TRACING': '0',
            'FW_ENABLE_TEXT_LOGGING': '1',
            'FW_PORT_SERIALIZATION': '0',
            'FW_ASSERT_LEVEL': 'FW_FILENAME_ASSERT',
        },
    }
}

BASE_REG_TRC_SER_RTGR_CMD = {
    **BASE,
    **{
        'tag': 'base,reg,trc,ser,rtgr,cmd',
        AC_CONSTANTS_FPP: {
            'PassiveRateGroupOutputPorts': '4',
            'CmdDispatcherComponentCommandPorts': '10',
            'StaticMemoryAllocations': '4',
        },

        FP_CONFIG_H: {
            'FW_OBJECT_NAMES': '1',
            'FW_OBJECT_REGISTRATION': '0',
            'FW_PORT_TRACING': '0',
            'FW_ENABLE_TEXT_LOGGING': '1',
            'FW_PORT_SERIALIZATION': '0',
            'FW_ASSERT_LEVEL': 'FW_FILENAME_ASSERT',
        },
    }
}

BASE_REG_TRC_SER_RTGR_CMD_BUF = {
    **BASE,
    **{
        'tag': 'base,reg,trc,ser,rtgr,cmd,buf',
        AC_CONSTANTS_FPP: {
            'PassiveRateGroupOutputPorts': '4',
            'CmdDispatcherComponentCommandPorts': '10',
            'StaticMemoryAllocations': '2',
        },

        FP_CONFIG_H: {
            'FW_OBJECT_NAMES': '1',
            'FW_OBJECT_REGISTRATION': '0',
            'FW_PORT_TRACING': '0',
            'FW_ENABLE_TEXT_LOGGING': '1',
            'FW_PORT_SERIALIZATION': '0',
            'FW_ASSERT_LEVEL': 'FW_FILENAME_ASSERT',
        },
        STATIC_MEMORY_CONFIG_HPP: {
            'STATIC_MEMORY_ALLOCATION_SIZE': 1024,
        },
    }
}

BASE_REG_TRC_SER_RTGR_CMD_BUF_TLM = {
    **BASE,
    **{
        'tag': 'base,reg,trc,ser,rtgr,cmd,buf,tlm',
        AC_CONSTANTS_FPP: {
            'PassiveRateGroupOutputPorts': '4',
            'CmdDispatcherComponentCommandPorts': '10',
            'StaticMemoryAllocations': '2',
        },

        FP_CONFIG_H: {
            'FW_OBJECT_NAMES': '1',
            'FW_OBJECT_REGISTRATION': '0',
            'FW_PORT_TRACING': '0',
            'FW_ENABLE_TEXT_LOGGING': '1',
            'FW_PORT_SERIALIZATION': '0',
            'FW_ASSERT_LEVEL': 'FW_FILENAME_ASSERT',
        },
        STATIC_MEMORY_CONFIG_HPP: {
            'STATIC_MEMORY_ALLOCATION_SIZE': 1024,
        },
        TLM_CHAN_IMPL_CFG_HPP: {
            'TLMCHAN_HASH_BUCKETS': 35,
        },
    }
}

BASE_REG_TRC_SER_RTGR_CMD_BUF_TLM_HEAP = {
    **BASE,
    **{
        'tag': 'base,reg,trc,ser,rtgr,cmd,buf,tlm,heap',
        AC_CONSTANTS_FPP: {
            'PassiveRateGroupOutputPorts': '4',
            'CmdDispatcherComponentCommandPorts': '10',
            'StaticMemoryAllocations': '2',
        },

        FP_CONFIG_H: {
            'FW_OBJECT_NAMES': '1',
            'FW_OBJECT_REGISTRATION': '0',
            'FW_PORT_TRACING': '0',
            'FW_ENABLE_TEXT_LOGGING': '1',
            'FW_PORT_SERIALIZATION': '0',
            'FW_ASSERT_LEVEL': 'FW_FILENAME_ASSERT',
        },
        STATIC_MEMORY_CONFIG_HPP: {
            'STATIC_MEMORY_ALLOCATION_SIZE': 1024,
        },
        TLM_CHAN_IMPL_CFG_HPP: {
            'TLMCHAN_HASH_BUCKETS': 35,
        },
        PRJ_CONF: {
            'CONFIG_HEAP_MEM_POOL_SIZE': 35000,
        },
    }
}

BASE_REG_TRC_SER_RTGR_CMD_BUF_TLM_HEAP_CRC = {
    **BASE,
    **{
        'tag': 'base,reg,trc,ser,rtgr,cmd,buf,tlm,heap,crc',
        AC_CONSTANTS_FPP: {
            'PassiveRateGroupOutputPorts': '4',
            'CmdDispatcherComponentCommandPorts': '10',
            'StaticMemoryAllocations': '2',
        },

        FP_CONFIG_H: {
            'FW_OBJECT_NAMES': '1',
            'FW_OBJECT_REGISTRATION': '0',
            'FW_PORT_TRACING': '0',
            'FW_ENABLE_TEXT_LOGGING': '1',
            'FW_PORT_SERIALIZATION': '0',
            'FW_ASSERT_LEVEL': 'FW_FILEID_ASSERT',
        },
        STATIC_MEMORY_CONFIG_HPP: {
            'STATIC_MEMORY_ALLOCATION_SIZE': 1024,
        },
        TLM_CHAN_IMPL_CFG_HPP: {
            'TLMCHAN_HASH_BUCKETS': 35,
        },
        PRJ_CONF: {
            'CONFIG_HEAP_MEM_POOL_SIZE': 35000,
        },
    }
}

BASE_REG_TRC_SER_RTGR_CMD_BUF_TLM_HEAP_CRC_LOG = {
    **BASE,
    **{
        'tag': 'base,reg,trc,ser,rtgr,cmd,buf,tlm,heap,crc,log',
        AC_CONSTANTS_FPP: {
            'PassiveRateGroupOutputPorts': '4',
            'CmdDispatcherComponentCommandPorts': '10',
            'StaticMemoryAllocations': '2',
        },

        FP_CONFIG_H: {
            'FW_OBJECT_NAMES': '1',
            'FW_OBJECT_REGISTRATION': '0',
            'FW_PORT_TRACING': '0',
            'FW_ENABLE_TEXT_LOGGING': '0',
            'FW_PORT_SERIALIZATION': '0',
            'FW_ASSERT_LEVEL': 'FW_FILEID_ASSERT',
        },
        STATIC_MEMORY_CONFIG_HPP: {
            'STATIC_MEMORY_ALLOCATION_SIZE': 1024,
        },
        TLM_CHAN_IMPL_CFG_HPP: {
            'TLMCHAN_HASH_BUCKETS': 35,
        },
        PRJ_CONF: {
            'CONFIG_HEAP_MEM_POOL_SIZE': 35000,
        },
        INSTANCES_FPP: {
            'COMMENT_OUT_TEXT_LOGGER': '#',
        },
        TOPOLOGY_FPP: {
            'COMMENT_OUT_TEXT_LOGGER': '#',
        },
        SETTINGS_INI: {
            'FPRIME_ENABLE_TEXT_LOGGERS': 'OFF',
        },
    }
}

BASE_REG_TRC_SER_RTGR_CMD_BUF_TLM_HEAP_CRC_LOG_OBJ = {
    **BASE,
    **{
        'tag': 'base,reg,trc,ser,rtgr,cmd,buf,tlm,heap,crc,log,obj',
        AC_CONSTANTS_FPP: {
            'PassiveRateGroupOutputPorts': '4',
            'CmdDispatcherComponentCommandPorts': '10',
            'StaticMemoryAllocations': '2',
        },

        FP_CONFIG_H: {
            'FW_OBJECT_NAMES': '0',
            'FW_OBJECT_REGISTRATION': '0',
            'FW_PORT_TRACING': '0',
            'FW_ENABLE_TEXT_LOGGING': '0',
            'FW_PORT_SERIALIZATION': '0',
            'FW_ASSERT_LEVEL': 'FW_FILEID_ASSERT',
        },
        STATIC_MEMORY_CONFIG_HPP: {
            'STATIC_MEMORY_ALLOCATION_SIZE': 1024,
        },
        TLM_CHAN_IMPL_CFG_HPP: {
            'TLMCHAN_HASH_BUCKETS': 35,
        },
        PRJ_CONF: {
            'CONFIG_HEAP_MEM_POOL_SIZE': 35000,
        },
        INSTANCES_FPP: {
            'COMMENT_OUT_TEXT_LOGGER': '#',
        },
        TOPOLOGY_FPP: {
            'COMMENT_OUT_TEXT_LOGGER': '#',
        },
        SETTINGS_INI: {
            'FPRIME_ENABLE_TEXT_LOGGERS': 'OFF',
        },
    }
}


BASE_REG_TRC_SER_RTGR_CMD_BUF_TLM_HEAP_CRC_LOG_OBJ_ASRT = {
    **BASE,
    **{
        'tag': 'base,reg,trc,ser,rtgr,cmd,buf,tlm,heap,crc,log,obj,asrt',
        AC_CONSTANTS_FPP: {
            'PassiveRateGroupOutputPorts': '4',
            'CmdDispatcherComponentCommandPorts': '10',
            'StaticMemoryAllocations': '2',
        },

        FP_CONFIG_H: {
            'FW_OBJECT_NAMES': '0',
            'FW_OBJECT_REGISTRATION': '0',
            'FW_PORT_TRACING': '0',
            'FW_ENABLE_TEXT_LOGGING': '0',
            'FW_PORT_SERIALIZATION': '0',
            'FW_ASSERT_LEVEL': 'FW_NO_ASSERT',
        },
        STATIC_MEMORY_CONFIG_HPP: {
            'STATIC_MEMORY_ALLOCATION_SIZE': 1024,
        },
        TLM_CHAN_IMPL_CFG_HPP: {
            'TLMCHAN_HASH_BUCKETS': 35,
        },
        PRJ_CONF: {
            'CONFIG_HEAP_MEM_POOL_SIZE': 35000,
        },
        INSTANCES_FPP: {
            'COMMENT_OUT_TEXT_LOGGER': '#',
        },
        TOPOLOGY_FPP: {
            'COMMENT_OUT_TEXT_LOGGER': '#',
        },
        SETTINGS_INI: {
            'FPRIME_ENABLE_TEXT_LOGGERS': 'OFF',
        },
    }
}


def backup_files(paths, backup_dir):
    """
    Back up the specified files to the backup directory.
    
    Args:
        paths (list): A list of file paths to be backed up.
        backup_dir (str): The directory where backup files will be stored.
    """
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    for path in paths:
        file_name = os.path.basename(path)
        shutil.copy2(path, os.path.join(backup_dir, file_name))

def restore_backups(paths, backup_dir):
    """
    Restore files from the backup directory to their original locations.
    
    Args:
        paths (list): A list of file paths to be restored.
        backup_dir (str): The directory where backup files are be stored.
    """

    for path in paths:
        file_name = os.path.basename(path)
        shutil.copy2(os.path.join(backup_dir, file_name), path)

def generate(replacements):
    for fname in TEMPLATES.keys():
        # Read the template file
        with open(TEMPLATES[fname][TMPL], 'r') as file:
            template_content = file.read()


        # Perform the substitution if needed
        if replacements[fname] is not None:
            # Create a template from the content
            template = Template(template_content)
            result = template.substitute(replacements[fname])
        else:
            result = template_content

        # Save the modified content to the output file
        with open(TEMPLATES[fname][TARGET], 'w') as file:
            file.write(result)

        print(f"File '{TEMPLATES[fname][TARGET]}' has been generated.")

def build_project(stats_output_dir):
    if not os.path.exists(stats_output_dir):
        os.makedirs(stats_output_dir)

    command = (f'rm -rf {LED_BLINKER_PATH}/build-*'
               f' && fprime-util generate -r {LED_BLINKER_PATH} -DBOARD=nucleo_h723zg -DCMAKE_GENERATOR=Ninja'
               f' && fprime-util build -p {LED_BLINKER_PATH} -j16'
               f' && rm {LED_BLINKER_PATH}/build-fprime-automatic-zephyr/zephyr/zephyr.elf'
               f' && ninja -C {LED_BLINKER_PATH}/build-fprime-automatic-zephyr zephyr.elf > {stats_output_dir}/compact.txt'
               f' && echo rom_report && west build --build-dir {LED_BLINKER_PATH}/build-fprime-automatic-zephyr/ -t rom_report > {stats_output_dir}/rom_usage.txt'
               f' && echo ram_report && west build --build-dir {LED_BLINKER_PATH}/build-fprime-automatic-zephyr/ -t ram_report > {stats_output_dir}/ram_usage.txt'
               f' && cp {LED_BLINKER_PATH}/build-fprime-automatic-zephyr/zephyr/zephyr.elf {stats_output_dir}/zephyr.elf'
    )

    try:
        # Run the command
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with return code {e.returncode}")
        raise e
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise e


# RUN ALL BENCHMARKS
templated_targets = [TEMPLATES[fname][TARGET] for fname in TEMPLATES]
benchmarks = [
    BASE, # Baseline
    BASE_REG,
    BASE_REG_TRC,
    BASE_REG_TRC_SER,
    BASE_REG_TRC_SER_RTGR,
    BASE_REG_TRC_SER_RTGR_CMD,
    BASE_REG_TRC_SER_RTGR_CMD_BUF,
    BASE_REG_TRC_SER_RTGR_CMD_BUF_TLM,
    BASE_REG_TRC_SER_RTGR_CMD_BUF_TLM_HEAP, # Dev
    BASE_REG_TRC_SER_RTGR_CMD_BUF_TLM_HEAP_CRC,
    BASE_REG_TRC_SER_RTGR_CMD_BUF_TLM_HEAP_CRC_LOG,
    BASE_REG_TRC_SER_RTGR_CMD_BUF_TLM_HEAP_CRC_LOG_OBJ,
    BASE_REG_TRC_SER_RTGR_CMD_BUF_TLM_HEAP_CRC_LOG_OBJ_ASRT # Min
]

backup_files(templated_targets, BACKUP_PATH)

try:
    for bench in benchmarks:
        print('Generating benchmark: ' + bench['tag'])
        generate(bench)
        build_project(os.path.join(REPORT_PATH, bench['tag']))
finally:
    restore_backups(templated_targets, BACKUP_PATH)