import os
import re

REPORT = 'report'

FILES = [
    {
        'name': 'Baseline',
        'path': os.path.join(REPORT, 'base')
    },
    {
        'name': 'Dev',
        'path': os.path.join(REPORT, 'base,reg,trc,ser,rtgr,cmd,buf,tlm,heap')
    },
    {
        'name': 'Min',
        'path': os.path.join(REPORT, 'base,reg,trc,ser,rtgr,cmd,buf,tlm,heap,crc,log,obj,asrt')
    }
]

COMPONENTS = [
    ['ActiveLogger', '_ZN10LedBlinker11eventLoggerE'],
    ['BufferManager','_ZN10LedBlinker23fileUplinkBufferManagerE'],
    ['CmdDispatcher', '_ZN10LedBlinker7cmdDispE'],
    ['CmdSequencer', '_ZN10LedBlinker6cmdSeqE'],
    ['Framer','_ZN10LedBlinker6uplinkE'],
    ['Deframer', '_ZN10LedBlinker8downlinkE'],
    ['FileManager', '_ZN10LedBlinker11fileManagerE'],
    ['FileUplink', '_ZN10LedBlinker10fileUplinkE'],
    ['FileDownlink', '_ZN10LedBlinker12fileDownlinkE'],
    ['PassiveRateGroup', '_ZN10LedBlinker10rateGroup2E'],
    ['TlmChan', '_ZN10LedBlinker7tlmSendE'],
    ['FileDownlinkPorts', None]
]
result = {}

for fobj in FILES:
    # Open the file in read mode
    with open(os.path.join(fobj['path'], 'rom_usage.txt'), 'r') as file:
        # Read the entire content of the file
        input_rom = file.read()

    with open(os.path.join(fobj['path'], 'ram_usage.txt'), 'r') as file:
        # Read the entire content of the file
        input_ram = file.read()

    for comp, compMangled in COMPONENTS:
        # print(comp, compMangled)
        # ROM
        # Define the regex pattern to match the line containing the target input and value
        pattern = re.compile(fr'\b{re.escape(comp)}\s+(\d+)')

        # Search for the pattern in the input text
        extracted_value = re.findall(pattern, input_rom)
        for value in extracted_value:
            result.setdefault(comp, {}).setdefault('rom', {}).setdefault(fobj['name'], []).append(int(value))

        # RAM
        pattern = re.compile(fr'\b{re.escape(compMangled if compMangled else "NOTEXISTENTTTHIHI")}\s+(\d+)')

        # Search for the pattern in the input text
        extracted_value = re.findall(pattern, input_ram)
        for value in (extracted_value if extracted_value else [0]):
            result.setdefault(comp, {}).setdefault('ram', {}).setdefault(fobj['name'], []).append(int(value))

# A hack to add the FileDownlinkPort size to FileDownlink
for fobj in FILES:
    result['FileDownlink']['rom'][fobj['name']][0] += result['FileDownlinkPorts']['rom'][fobj['name']][0]

del result['FileDownlinkPorts']
print(result)

for comp, compMangled in COMPONENTS:
    if comp == 'FileDownlinkPorts':
        continue

    print(f"{comp} & {sum(result[comp]['rom']['Dev'])} & {sum(result[comp]['rom']['Min'])} & {sum(result[comp]['ram']['Dev'])} & {sum(result[comp]['ram']['Min'])}", end='')
    print(' \\\\')