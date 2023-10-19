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
}

# Define the replacement values
BASELINE = {
    AC_CONSTANTS_FPP: {
        'PassiveRateGroupOutputPorts': '199',
        'CmdDispatcherComponentCommandPorts': '10',
        'StaticMemoryAllocations': '8',
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
    for fname in replacements:
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

    command = (f'rm -rf {LED_BLINKER_PATH}/build-* && '
               f'fprime-util generate -r {LED_BLINKER_PATH} -DBOARD=nucleo_h723zg -DCMAKE_GENERATOR=Ninja &&'
               f'west build --build-dir {LED_BLINKER_PATH}/build-fprime-automatic-zephyr/ -t zephyr.elf &&'
               f'rm {LED_BLINKER_PATH}/build-fprime-automatic-zephyr/zephyr/zephyr.elf &&'
               f'ninja -C {LED_BLINKER_PATH}/build-fprime-automatic-zephyr zephyr.elf > {stats_output_dir}/compact.txt &&'
               f'echo rom_report && west build --build-dir {LED_BLINKER_PATH}/build-fprime-automatic-zephyr/ -t rom_report > {stats_output_dir}/rom_usage.txt &&'
               f'echo ram_report && west build --build-dir {LED_BLINKER_PATH}/build-fprime-automatic-zephyr/ -t ram_report > {stats_output_dir}/ram_usage.txt'
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
all_targets = [TEMPLATES[fname][TARGET] for fname in TEMPLATES]

backup_files(all_targets, BACKUP_PATH)
try:
    generate(BASELINE)
    build_project(os.path.join(REPORT_PATH, 'baseline'))
finally:
    restore_backups(all_targets, BACKUP_PATH)