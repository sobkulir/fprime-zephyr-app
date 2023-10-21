import os
import re

# DEV_PATH = 'report/base,reg,trc,ser,rtgr,cmd,buf,tlm,heap'
# DEV_PATH = 'report/base'
DEV_PATH = 'report/base,reg,trc,ser,rtgr,cmd,buf,tlm,heap,crc,log,obj,asrt'

RAM_PARTS = {
    'Components': [
        '_ZL8led_gpio', 
        '_ZN10LedBlinker10fileUplinkE', 
        '_ZN10LedBlinker10rateGroup1E', 
        '_ZN10LedBlinker10rateGroup2E', 
        '_ZN10LedBlinker10rateGroup3E', 
        '_ZN10LedBlinker10textLoggerE', 
        '_ZN10LedBlinker10zephyrTimeE', 
        '_ZN10LedBlinker11eventLoggerE', 
        '_ZN10LedBlinker11fileManagerE', 
        '_ZN10LedBlinker12fileDownlinkE', 
        '_ZN10LedBlinker12staticMemoryE', 
        '_ZN10LedBlinker13ledGpioDriverE', 
        '_ZN10LedBlinker14commUartDriverE', 
        '_ZN10LedBlinker15rateGroupDriverE', 
        '_ZN10LedBlinker16zephyrRateDriverE', 
        '_ZN10LedBlinker23fileUplinkBufferManagerE', 
        '_ZN10LedBlinker3ledE', 
        '_ZN10LedBlinker5prmDbE', 
        '_ZN10LedBlinker6cmdSeqE', 
        '_ZN10LedBlinker6uplinkE', 
        '_ZN10LedBlinker7cmdDispE', 
        '_ZN10LedBlinker7tlmSendE', 
        '_ZN10LedBlinker8downlinkE', 
        '_ZN2Fw6Logger16s_current_loggerE', 
        '_ZN2Fw9ZERO_TIMEE', 
        '_ZN2FwL12s_assertHookE', 
        '_ZN2Os4Task10s_numTasksE', 
        '_ZN2Os4Task14s_taskRegistryE', 
        '_ZN2Os5Queue11s_numQueuesE',
        ],
    'Component Stacks': [
        '_ZN10LedBlinker12_GLOBAL__N_113ConfigObjects10fileUplink5stackE', 
        '_ZN10LedBlinker12_GLOBAL__N_113ConfigObjects11eventLogger5stackE', 
        '_ZN10LedBlinker12_GLOBAL__N_113ConfigObjects11fileManager5stackE', 
        '_ZN10LedBlinker12_GLOBAL__N_113ConfigObjects12fileDownlink5stackE', 
        '_ZN10LedBlinker12_GLOBAL__N_113ConfigObjects5prmDb5stackE', 
        '_ZN10LedBlinker12_GLOBAL__N_113ConfigObjects6cmdSeq5stackE', 
        '_ZN10LedBlinker12_GLOBAL__N_113ConfigObjects7cmdDisp5stackE', 
        '_ZN10LedBlinker12_GLOBAL__N_113ConfigObjects7tlmSend5stackE', 
    ],
    'F Prime Aux': [
        'fprime-zephyr-app',
        'fprime',
    ],
    'Zephyr Aux': [
        '__compound_literal.0',
        '__global_locale',
        '_impure_ptr',
        '_kernel',
        'dynamic_regions.0',
        'errno',
        'impure_data',
        'partitions.0',
        'sched_spinlock',
        'stm32h7_flash_layout.0',
        'lib',
    ],
    'Zephyr drivers_fs_debug_etc': [
        'drivers',
        'subsys',
    ],
    'Zephyr stacks and threads': [
        '_sw_isr_table',
        'z_interrupt_stacks',
        'z_idle_threads',
        'z_main_thread',
        'z_idle_stacks',
        'z_main_stack',
    ],
    'Heap': [
        'mempool.c',
        '__malloc_av_',
        '__malloc_current_mallinfo',
        '__malloc_max_sbrked_mem',
        '__malloc_max_total_mem',
        '__malloc_sbrk_base',
        '__malloc_top_pad',
        '__malloc_trim_threshold',

    ],

}

FLASH_PARTS = {
    'F Prime Drv,etc,Os,Topology': [
        'Drv',
        'Os',
        'LedBlinker',
        'CFDP',
        'Utils',
        'Fw',

    ],
    'F Prime Components': [
        'Components',
        'Svc',
        '_ZL8led_gpio',
        '_ZN10LedBlinker14loadParametersEv',
        '_ZN3Svc25FileDownlinkComponentBase31getNum_FileComplete_OutputPortsEv',
        '_ZN3Svc30CommandDispatcherComponentBase31getNum_seqCmdStatus_OutputPortsEv',
        '_ZTVN10Components22LedDriverComponentBaseE',
        '_ZTVN10Components9LedDriverE',
        '_ZTVN2Fw10ParamValidE',
        '_ZTVN2Fw10StringBaseE',
        '_ZTVN2Fw11CmdResponseE',
        '_ZTVN2Fw11LogSeverityE',
        '_ZTVN2Fw11ParamBufferE',
        '_ZTVN2Fw12CmdArgBufferE',
        '_ZTVN2Fw12CmdStringArgE',
        '_ZTVN2Fw12InputCmdPortE',
        '_ZTVN2Fw12InputComPortE',
        '_ZTVN2Fw12InputLogPortE',
        '_ZTVN2Fw12InputTlmPortE',
        '_ZTVN2Fw12LogStringArgE',
        '_ZTVN2Fw12MemAllocatorE',
        '_ZTVN2Fw12SerialBufferE',
        '_ZTVN2Fw12SerializableE',
        '_ZTVN2Fw13InputPortBaseE',
        '_ZTVN2Fw13InputTimePortE',
        '_ZTVN2Fw13OutputCmdPortE',
        '_ZTVN2Fw13OutputComPortE',
        '_ZTVN2Fw13OutputLogPortE',
        '_ZTVN2Fw13OutputTlmPortE',
        '_ZTVN2Fw13TextLogStringE',
        '_ZTVN2Fw14DeserialStatusE',
        '_ZTVN2Fw14OutputPortBaseE',
        '_ZTVN2Fw14OutputTimePortE',
        '_ZTVN2Fw15InputCmdRegPortE',
        '_ZTVN2Fw15InputPrmGetPortE',
        '_ZTVN2Fw15InputPrmSetPortE',
        '_ZTVN2Fw15InputTlmGetPortE',
        '_ZTVN2Fw16InputLogTextPortE',
        '_ZTVN2Fw16OutputCmdRegPortE',
        '_ZTVN2Fw17OutputLogTextPortE',
        '_ZTVN2Fw18InputBufferGetPortE',
        '_ZTVN2Fw19ActiveComponentBaseE',
        '_ZTVN2Fw19InputBufferSendPortE',
        '_ZTVN2Fw19OutputBufferGetPortE',
        '_ZTVN2Fw19QueuedComponentBaseE',
        '_ZTVN2Fw19SerializeBufferBaseE',
        '_ZTVN2Fw20InputCmdResponsePortE',
        '_ZTVN2Fw20OutputBufferSendPortE',
        '_ZTVN2Fw20PassiveComponentBaseE',
        '_ZTVN2Fw21OutputCmdResponsePortE',
        '_ZTVN2Fw21ZephyrMallocAllocatorE',
        '_ZTVN2Fw23ExternalSerializeBufferE',
        '_ZTVN2Fw25InputSuccessConditionPortE',
        '_ZTVN2Fw26OutputSuccessConditionPortE',
        '_ZTVN2Fw4TimeE',
        '_ZTVN2Fw5LogicE',
        '_ZTVN2Fw6BufferE',
        '_ZTVN2Fw6StringE',
        '_ZTVN2Fw7ObjBaseE',
        '_ZTVN2Fw7SuccessE',
        '_ZTVN2Fw8PortBaseE',
        '_ZTVN2Fw9CmdPacketE',
        '_ZTVN2Fw9ComBufferE',
        '_ZTVN2Fw9ComPacketE',
        '_ZTVN2Fw9LogBufferE',
        '_ZTVN2Fw9LogPacketE',
        '_ZTVN2Fw9TlmBufferE',
        '_ZTVN2Fw9TlmPacketE',
        '_ZTVN2Os10TaskStringE',
        '_ZTVN2Os11QueueStringE',
        '_ZTVN2Os3LogE',
        '_ZTVN2Os4FileE',
        '_ZTVN2Os4TaskE',
        '_ZTVN2Os5MutexE',
        '_ZTVN2Os5QueueE',
        '_ZTVN3Drv10PollStatusE',
        '_ZTVN3Drv10RecvStatusE',
        '_ZTVN3Drv10SendStatusE',
        '_ZTVN3Drv16ZephyrGpioDriverE',
        '_ZTVN3Drv16ZephyrGpioStatusE',
        '_ZTVN3Drv16ZephyrRateDriverE',
        '_ZTVN3Drv16ZephyrUartDriverE',
        '_ZTVN3Drv23InputByteStreamRecvPortE',
        '_ZTVN3Drv23InputByteStreamSendPortE',
        '_ZTVN3Drv23InputZephyrGpioReadPortE',
        '_ZTVN3Drv24InputZephyrGpioWritePortE',
        '_ZTVN3Drv24OutputByteStreamPollPortE',
        '_ZTVN3Drv24OutputByteStreamRecvPortE',
        '_ZTVN3Drv24OutputByteStreamSendPortE',
        '_ZTVN3Drv25OutputByteStreamReadyPortE',
        '_ZTVN3Drv25OutputZephyrGpioWritePortE',
        '_ZTVN3Drv29ZephyrGpioDriverComponentBaseE',
        '_ZTVN3Drv29ZephyrRateDriverComponentBaseE',
        '_ZTVN3Drv29ZephyrUartDriverComponentBaseE',
        '_ZTVN3Svc10FileUplinkE',
        '_ZTVN3Svc11FileManagerE',
        '_ZTVN3Svc12FileDownlinkE',
        '_ZTVN3Svc12_GLOBAL__N_113WorkingBufferE',
        '_ZTVN3Svc12_GLOBAL__N_130ComponentIpcSerializableBufferE',
        '_ZTVN3Svc13FprimeFramingE',
        '_ZTVN3Svc13InputPingPortE',
        '_ZTVN3Svc14InputCyclePortE',
        '_ZTVN3Svc14InputSchedPortE',
        '_ZTVN3Svc14OutputPingPortE',
        '_ZTVN3Svc14SendFileStatusE',
        '_ZTVN3Svc14ZephyrTimeImplE',
        '_ZTVN3Svc15FprimeDeframingE',
        '_ZTVN3Svc15FramingProtocolE',
        '_ZTVN3Svc15OutputCyclePortE',
        '_ZTVN3Svc15OutputSchedPortE',
        '_ZTVN3Svc15RateGroupDriverE',
        '_ZTVN3Svc16ActiveLoggerImplE',
        '_ZTVN3Svc16PassiveRateGroupE',
        '_ZTVN3Svc16SendFileResponseE',
        '_ZTVN3Svc17DeframingProtocolE',
        '_ZTVN3Svc17InputCmdSeqInPortE',
        '_ZTVN3Svc17TimeComponentBaseE',
        '_ZTVN3Svc18PrmDbComponentBaseE',
        '_ZTVN3Svc19FramerComponentBaseE',
        '_ZTVN3Svc19PrmDb_PrmWriteErrorE',
        '_ZTVN3Svc20ActiveLogger_EnabledE',
        '_ZTVN3Svc20CmdSequencer_SeqModeE',
        '_ZTVN3Svc20OutputFatalEventPortE',
        '_ZTVN3Svc20TlmChanComponentBaseE',
        '_ZTVN3Svc21CommandDispatcherImplE',
        '_ZTVN3Svc21ConsoleTextLoggerImplE',
        '_ZTVN3Svc21DeframerComponentBaseE',
        '_ZTVN3Svc21InputCmdSeqCancelPortE',
        '_ZTVN3Svc23CmdSequencer_BlockStateE',
        '_ZTVN3Svc23FileUplinkComponentBaseE',
        '_ZTVN3Svc24FileManagerComponentBaseE',
        '_ZTVN3Svc24InputSendFileRequestPortE',
        '_ZTVN3Svc25ActiveLoggerComponentBaseE',
        '_ZTVN3Svc25CmdSequencerComponentBaseE',
        '_ZTVN3Svc25CmdSequencerComponentImpl14FPrimeSequenceE',
        '_ZTVN3Svc25CmdSequencerComponentImpl8SequenceE',
        '_ZTVN3Svc25CmdSequencerComponentImplE',
        '_ZTVN3Svc25FileDownlinkComponentBaseE',
        '_ZTVN3Svc25StaticMemoryComponentBaseE',
        '_ZTVN3Svc25StaticMemoryComponentImplE',
        '_ZTVN3Svc26BufferManagerComponentBaseE',
        '_ZTVN3Svc26BufferManagerComponentImplE',
        '_ZTVN3Svc26CmdSequencer_FileReadStageE',
        '_ZTVN3Svc26OutputSendFileCompletePortE',
        '_ZTVN3Svc27ActiveLogger_FilterSeverityE',
        '_ZTVN3Svc28RateGroupDriverComponentBaseE',
        '_ZTVN3Svc29PassiveRateGroupComponentBaseE',
        '_ZTVN3Svc30CommandDispatcherComponentBaseE',
        '_ZTVN3Svc30PassiveTextLoggerComponentBaseE',
        '_ZTVN3Svc6FramerE',
        '_ZTVN3Svc7TlmChanE',
        '_ZTVN3Svc8DeframerE',
        '_ZTVN3Svc8TimerValE',
        '_ZTVN3Svc9PrmDbImplE',
        '_ZTVN5Utils10HashBufferE',
        '_ZThn768_N3Svc6Framer4sendERN2Fw6BufferE',
        '_ZThn768_N3Svc6Framer8allocateEj',
        '_ZThn768_N3Svc6FramerD0Ev',
        '_ZThn768_N3Svc6FramerD1Ev',
        '_ZThn952_N3Svc8Deframer5routeERN2Fw6BufferE',
        '_ZThn952_N3Svc8Deframer8allocateEj',
        '_ZThn952_N3Svc8DeframerD0Ev',
        '_ZThn952_N3Svc8DeframerD1Ev',
        '_ZZN3Svc9PrmDbImpl24PRM_SAVE_FILE_cmdHandlerEjjE5delim',
        '_ZdlPv',
    ],

    'Zephyr Aux': [
        'opt',
        'CSWTCH.2898',
        'CSWTCH.2900',
        'CSWTCH.3   ',
        'CSWTCH.4   ',
        'CSWTCH.487 ',
        'CSWTCH.672 ',
        'SystemCoreClock     ',
        '_Balloc     ',
        '_Bfree     ',
        '_GLOBAL__sub_I__ZN10LedBlinker7cmdDispE     ',
        '_GLOBAL__sub_I__ZN2Fw9ZERO_TIMEE     ',
        '_GLOBAL__sub_I_logger     ',
        '_ZL11spi_nwp_pin     ',
        '_ZL13spi_nhold_pin     ',
        '__aeabi_idiv0  ',
        '__ascii_mbtowc  ',
        '__ascii_wctomb  ',
        '__assert_func  ',
        '__compound_literal.0',
        '__d2b  ',
        '__device_dts_ord_122  ',
        '__device_dts_ord_126  ',
        '__device_dts_ord_127  ',
        '__device_dts_ord_128  ',
        '__device_dts_ord_129  ',
        '__device_dts_ord_130  ',
        '__device_dts_ord_131  ',
        '__device_dts_ord_132  ',
        '__device_dts_ord_31  ',
        '__device_dts_ord_35  ',
        '__device_dts_ord_36  ',
        '__device_dts_ord_41  ',
        '__device_dts_ord_45  ',
        '__device_dts_ord_47  ',
        '__device_dts_ord_51  ',
        '__device_dts_ord_80  ',
        '__device_dts_ord_9  ',
        '__device_dts_ord_90  ',
        '__device_dts_ord_93  ',
        '__func__.0',
        '__global_locale  ',
        '__hi0bits  ',
        '__i2b  ',
        '__lo0bits  ',
        '__lshift  ',
        '__malloc_av_  ',
        '__malloc_lock  ',
        '__malloc_sbrk_base  ',
        '__malloc_trim_threshold  ',
        '__malloc_unlock  ',
        '__mcmp  ',
        '__mdiff  ',
        '__mprec_bigtens  ',
        '__mprec_tens  ',
        '__multadd  ',
        '__multiply  ',
        '__popcountsi2  ',
        '__pow5mult  ',
        '__retarget_lock_close_recursive  ',
        '__sbprintf  ',
        '__sclose  ',
        '__sflush_r  ',
        '__sfvwrite_r  ',
        '__sinit  ',
        '__smakebuf_r  ',
        '__sprint_r  ',
        '__sread  ',
        '__sseek  ',
        '__ssprint_r  ',
        '__swrite  ',
        '__swsetup_r  ',
        '__udivmoddi4  ',
        '_calloc_r  ',
        '_cleanup_r  ',
        '_close  ',
        '_close_r  ',
        '_ctype_  ',
        '_dtoa_r  ',
        '_fflush_r  ',
        '_free_r  ',
        '_fstat_r  ',
        '_fwalk_reent  ',
        '_getpid_r  ',
        '_impure_ptr  ',
        '_isatty_r  ',
        '_kill_r  ',
        '_localeconv_r  ',
        '_lseek_r  ',
        '_malloc_r  ',
        '_malloc_trim_r  ',
        '_read_r  ',
        '_realloc_r  ',
        '_sbrk_r  ',
        '_svfprintf_r  ',
        '_sw_isr_table  ',
        '_vfiprintf_r  ',
        '_vfprintf_r  ',
        '_write_r  ',
        'abort  ',
        'blanks.1',
        'fiprintf  ',
        'fprintf  ',
        'free  ',
        'frexp  ',
        'impure_data  ',
        'levels.0',
        'line_range_0.6',
        'line_range_1.5',
        'line_range_2.4',
        'line_range_3.3',
        'line_range_4.2',
        'line_range_5.1',
        'line_range_6.0',
        'malloc  ',
        'memcmp  ',
        'memcpy  ',
        'memmove  ',
        'memset  ',
        'mpu_config  ',
        'p05.0',
        'partitions.0',
        'postfix.0',
        'prefix.1',
        'quorem  ',
        'raise  ',
        'rtable.0',
        'snprintf  ',
        'strchr  ',
        'strcspn  ',
        'strlen  ',
        'strncat  ',
        'strncmp  ',
        'strncpy  ',
        'strnlen  ',
        'strspn  ',
        'system  ',
        'vsnprintf  ',
        'zeroes.0',
        'zephyr',
        'include',
        'soc',
    ],
    'Zephyr Fs,deubg,logging,storage': {
        'arch',
        'drivers',
        'modules',
        'subsys'
    },
    'Zephyr kernel,lib': [
        'kernel',
        'lib',
    ],
    'String constants,other unnamed data': [
        'hidden',
    ]
}

def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


with open(os.path.join(DEV_PATH, 'ram_usage.txt'), 'r') as file:
    # Read the entire content of the file
    input_ram = file.read()

with open(os.path.join(DEV_PATH, 'rom_usage.txt'), 'r') as file:
    # Read the entire content of the file
    input_flash = file.read()


results = {
    'ram': {},
    'flash': {},
}

totalito = 0
for part_name, symbols in RAM_PARTS.items():
    results['ram'][part_name] = 0

    for s in symbols:
        pattern = re.compile(fr'\b{re.escape(s)}\s+(\d+)')

        # Search for the pattern in the input text
        extracted_value = re.findall(pattern, input_ram)
        # assert len(extracted_value) == 1, f"Found {len(extracted_value)} matches for {s}"
        if not extracted_value:
            continue
        results['ram'][part_name] += int(extracted_value[0])

    totalito += results['ram'][part_name]

print('ram totalito', totalito)
totalito = 0
for part_name, symbols in FLASH_PARTS.items():
    results['flash'][part_name] = 0

    for s in symbols:
        pattern = re.compile(fr'\b{re.escape(s)}\)?\s+(\d+)')

        # Search for the pattern in the input text
        extracted_value = re.findall(pattern, input_flash)
        # assert len(extracted_value) >= 1, f"Found {len(extracted_value)} matches for {s}"
        if not extracted_value:
            continue
        results['flash'][part_name] += sum(map(int,extracted_value))

    totalito += results['flash'][part_name]

print('flash totalito', totalito)

print('[')
for k,v in results['ram'].items():
    print(f'["{k}",{v}],')
print(']')

print()

print('[')
for k,v in results['flash'].items():
    print(f'["{k}",{v}],')
print(']')