import re

# Input text containing thread information
input_base = """Thread analyze:
 T_tlmSend           : STACK: unused 11456 usage 832 / 12288 (6 %); CPU: 1 %
      : Total CPU cycles used: 864258943
 T_prmDb             : STACK: unused 11440 usage 848 / 12288 (6 %); CPU: 0 %
      : Total CPU cycles used: 745
 T_fileUplink        : STACK: unused 11680 usage 608 / 12288 (4 %); CPU: 0 %
      : Total CPU cycles used: 1152
 T_fileManager       : STACK: unused 11344 usage 944 / 12288 (7 %); CPU: 0 %
      : Total CPU cycles used: 774
 T_fileDownlink      : STACK: unused 11248 usage 1040 / 12288 (8 %); CPU: 0 %
      : Total CPU cycles used: 286102
 T_eventLogger       : STACK: unused 11392 usage 896 / 12288 (7 %); CPU: 0 %
      : Total CPU cycles used: 740
 T_cmdSeq            : STACK: unused 11112 usage 1176 / 12288 (9 %); CPU: 0 %
      : Total CPU cycles used: 3716441
 T_cmdDisp           : STACK: unused 11376 usage 912 / 12288 (7 %); CPU: 0 %
      : Total CPU cycles used: 706
 thread_analyzer     : STACK: unused 432 usage 528 / 960 (55 %); CPU: 0 %
      : Total CPU cycles used: 9056889
 logging             : STACK: unused 248 usage 520 / 768 (67 %); CPU: 1 %
      : Total CPU cycles used: 1194110946
 idle                : STACK: unused 272 usage 48 / 320 (15 %); CPU: 96 %
      : Total CPU cycles used: 74307410491
 main                : STACK: unused 8684 usage 1252 / 9936 (12 %); CPU: 0 %
      : Total CPU cycles used: 755637527
 ISR0                : STACK: unused 1592 usage 520 / 2112 (24 %)
"""

input_after_10_seconds = """Thread analyze:                                                                                                                   
 T_tlmSend           : STACK: unused 11456 usage 832 / 12288 (6 %); CPU: 1 %                                                                                  
      : Total CPU cycles used: 924871429                                                                                                                      
 T_prmDb             : STACK: unused 11440 usage 848 / 12288 (6 %); CPU: 0 %                                                                                  
      : Total CPU cycles used: 745                                                                                                                            
 T_fileUplink        : STACK: unused 11680 usage 608 / 12288 (4 %); CPU: 0 %                                                                                  
      : Total CPU cycles used: 1152                                                                                                                           
 T_fileManager       : STACK: unused 11344 usage 944 / 12288 (7 %); CPU: 0 %                                                                                  
      : Total CPU cycles used: 774                                                                                                                            
 T_fileDownlink      : STACK: unused 11248 usage 1040 / 12288 (8 %); CPU: 0 %                                                                                 
      : Total CPU cycles used: 306663                                                                                                                         
 T_eventLogger       : STACK: unused 11392 usage 896 / 12288 (7 %); CPU: 0 %                                                                                  
      : Total CPU cycles used: 740                                                                                                                            
 T_cmdSeq            : STACK: unused 11112 usage 1176 / 12288 (9 %); CPU: 0 %                                                                                 
      : Total CPU cycles used: 3980148                                                                                                                        
 T_cmdDisp           : STACK: unused 11376 usage 912 / 12288 (7 %); CPU: 0 %
      : Total CPU cycles used: 706
 thread_analyzer     : STACK: unused 432 usage 528 / 960 (55 %); CPU: 0 %
      : Total CPU cycles used: 9666166
 logging             : STACK: unused 248 usage 520 / 768 (67 %); CPU: 1 %
      : Total CPU cycles used: 1264051885
 idle                : STACK: unused 272 usage 48 / 320 (15 %); CPU: 96 %
      : Total CPU cycles used: 79614803442
 main                : STACK: unused 8684 usage 1252 / 9936 (12 %); CPU: 0 %
      : Total CPU cycles used: 808998984
 ISR0                : STACK: unused 1592 usage 520 / 2112 (24 %)
"""


base_uplink = """Thread analyze:                                                                                                                                               
 T_tlmSend           : STACK: unused 11312 usage 912 / 12224 (7 %); CPU: 1 %                                                                                  
      : Total CPU cycles used: 83772497                                                                                                                       
 T_prmDb             : STACK: unused 11440 usage 848 / 12288 (6 %); CPU: 0 %                                                                                  
      : Total CPU cycles used: 717                                                                                                                            
 T_fileUplink        : STACK: unused 10736 usage 1488 / 12224 (12 %); CPU: 12 %                                                                               
      : Total CPU cycles used: 696171030                                                                                                                      
 T_fileManager       : STACK: unused 11344 usage 944 / 12288 (7 %); CPU: 0 %                                                                                  
      : Total CPU cycles used: 821                                                                                                                            
 T_fileDownlink      : STACK: unused 11248 usage 1040 / 12288 (8 %); CPU: 0 %                                                                                 
      : Total CPU cycles used: 22350                                                                                                                          
 T_eventLogger       : STACK: unused 11392 usage 896 / 12288 (7 %); CPU: 0 %                                                                                  
      : Total CPU cycles used: 751                                                                                                                            
 T_cmdSeq            : STACK: unused 11112 usage 1176 / 12288 (9 %); CPU: 0 %                                                                                 
      : Total CPU cycles used: 270859                                                                                                                         
 T_cmdDisp           : STACK: unused 11376 usage 912 / 12288 (7 %); CPU: 0 %                                                                                  
      : Total CPU cycles used: 768                                                                                                                            
 thread_analyzer     : STACK: unused 528 usage 432 / 960 (45 %); CPU: 0 %                                                                                     
      : Total CPU cycles used: 1140300                                                                                                                        
 logging             : STACK: unused 112 usage 592 / 704 (84 %); CPU: 5 %                                                                                     
      : Total CPU cycles used: 312499853                                                                                                                      
 idle                : STACK: unused 272 usage 48 / 320 (15 %); CPU: 79 %                                                                                     
      : Total CPU cycles used: 4576184617                                                                                                                     
 main                : STACK: unused 8664 usage 1272 / 9936 (12 %); CPU: 1 %                                                                                  
      : Total CPU cycles used: 69576593                                                                                                                       
 ISR0                : STACK: unused 1592 usage 520 / 2112 (24 %)
"""

after_10_second_uplink = """Thread analyze:                                                                                                                                               
 T_tlmSend           : STACK: unused 11312 usage 912 / 12224 (7 %); CPU: 1 %                                                                                  
      : Total CPU cycles used: 166592702                                                                                                                      
 T_prmDb             : STACK: unused 11440 usage 848 / 12288 (6 %); CPU: 0 %                                                                                  
      : Total CPU cycles used: 717                                                                                                                            
 T_fileUplink        : STACK: unused 10736 usage 1488 / 12224 (12 %); CPU: 29 %                                                                               
      : Total CPU cycles used: 3333441070                                                                                                                     
 T_fileManager       : STACK: unused 11344 usage 944 / 12288 (7 %); CPU: 0 %                                                                                  
      : Total CPU cycles used: 821                                                                                                                            
 T_fileDownlink      : STACK: unused 11248 usage 1040 / 12288 (8 %); CPU: 0 %                                                                                 
      : Total CPU cycles used: 43255                                                                                                                          
 T_eventLogger       : STACK: unused 11392 usage 896 / 12288 (7 %); CPU: 0 %                                                                                  
      : Total CPU cycles used: 751                                                                                                                            
 T_cmdSeq            : STACK: unused 11112 usage 1176 / 12288 (9 %); CPU: 0 %                                                                                 
      : Total CPU cycles used: 545089                                                                                                                         
 T_cmdDisp           : STACK: unused 11376 usage 912 / 12288 (7 %); CPU: 0 %                                                                                  
      : Total CPU cycles used: 768                                                                                                                            
 thread_analyzer     : STACK: unused 472 usage 488 / 960 (50 %); CPU: 0 %                                                                                     
      : Total CPU cycles used: 1754338                                                                                                                        
 logging             : STACK: unused 112 usage 592 / 704 (84 %); CPU: 3 %                                                                                     
      : Total CPU cycles used: 407586900                                                                                                                      
 idle                : STACK: unused 272 usage 48 / 320 (15 %); CPU: 63 %                                                                                     
      : Total CPU cycles used: 7173074319                                                                                                                     
 main                : STACK: unused 8664 usage 1272 / 9936 (12 %); CPU: 1 %                                                                                  
      : Total CPU cycles used: 148014811                                                                                                                      
 ISR0                : STACK: unused 1592 usage 520 / 2112 (24 %)  
"""
# Regular expressions to match thread information and total CPU cycles used
thread_info_pattern = r'(?P<thread_name>[\w_]+)\s+:\s+.*?CPU:\s+(?P<cpu_percent>\d+)\s+%\s*\n\s+:\sTotal CPU cycles used:\s+(?P<cpu_cycles>\d+)\s+'
total_cycles_pattern = r'Total CPU cycles used:\s+(?P<cpu_cycles>\d+)'

# Initialize variables to store thread information


# Find thread information
def get_cycles_per_thread(input_text): 
    res = {}     
    for match in re.finditer(thread_info_pattern, input_text, re.MULTILINE):
        thread_name = match.group('thread_name')
        cpu_cycles = int(match.group('cpu_cycles'))
        res[thread_name] = cpu_cycles
    return res

base = get_cycles_per_thread(input_base)
after_10_seconds = get_cycles_per_thread(input_after_10_seconds)

diff = { thread_name: after - base[thread_name] for thread_name, after in after_10_seconds.items()}

total = sum(diff.values())

# 48% during uplink is saving
# T_tlmSend: 1.5081762036794462%
# T_prmDb: 0.0%
# T_fileUplink: 48.025332912478795%
# T_fileManager: 0.0%
# T_fileDownlink: 0.0003806851665957458%
# T_eventLogger: 0.0%
# T_cmdSeq: 0.004993795419064882%
# T_cmdDisp: 0.0%
# thread_analyzer: 0.011181782268649536%
# logging: 1.7315583988659418%
# idle: 47.28999707422371%
# main: 1.428379147897796%

# 
# Bench fdown_uart_send result: 80.60, Raw: 1774538979                                                                                                          
# Bench fdown_file_read result: 16.87, Raw: 371373726                                                                                                           
# Bench tlm_run result: 1.41, Raw: 7775763                                                                                                                      
# Bench tlm_run result: 1.42, Raw: 7698975                                                                                                                      
# Bench tlm_run result: 1.42, Raw: 7782787                                                                                                                      
# Bench tlm_run result: 1.41, Raw: 7776579                                                                                                                      
# Bench fdown_uart_send result: 80.59, Raw: 1774553952                                                                                                          
# Bench fdown_file_read result: 16.89, Raw: 371884957                                                                                                           
# Bench tlm_run result: 1.41, Raw: 7776833                                                                                                                      
# Bench tlm_run result: 1.41, Raw: 7782932                                                                                                                      
# Bench tlm_run result: 1.42, Raw: 7786096                                                                                                                      
# Bench tlm_run result: 1.43, Raw: 7785758                                                                                                                      
# Bench fdown_uart_send result: 80.59, Raw: 1774514026                                                                                                          
# Bench fdown_file_read result: 16.87, Raw: 371520360                                                                                                           
# Bench tlm_run result: 1.42, Raw: 7786676                                                                                                                      
# Bench tlm_run result: 1.41, Raw: 7782989                                                                                                                      
# Bench tlm_run result: 1.42, Raw: 7786459                                                                                                                      
# Bench tlm_run result: 1.41, Raw: 7776067                                                                                                                      
# Bench fdown_uart_send result: 80.58, Raw: 1774507970                                                                                                          
# Bench fdown_file_read result: 16.89, Raw: 372066617

name_mapping = {
    'T_tlmSend': 'TlmChan',
    'T_prmDb': 'PrmDb',
    'T_fileUplink': 'FileUplink',
    'T_fileManager': 'FileManager',
    'T_fileDownlink': 'FileDownlink',
    'T_eventLogger': 'EventLogger',
    'T_cmdSeq': 'CmdSequencer',
    'T_cmdDisp': 'CmdDispatcher',
    'thread_analyzer': 'ThreadAnalyzer',
    'logging': 'Logging',
    'idle': 'Idle',
    'main': 'Main',
    'ISR0': 'ISR0'
}
for thread_name, cycles in sorted(diff.items(), key=lambda item: item[1], reverse=True):
    print(f"{name_mapping[thread_name]} & {round(100 * cycles / total, 4)}\\% \\\\")

print(f"\\textbf{'{'}Total{'}'} & {100 * (1 - diff['idle'] / total)}\\% \\\\")
# # Find total CPU cycles used
# for match in re.finditer(total_cycles_pattern, input_text):
#     thread_name = match.group('thread_name')
#     cpu_cycles = int(match.group('cpu_cycles'))
#     total_cycles[thread_name] = cpu_cycles

# # Calculate and print CPU cycle percentages
# for thread_name, cpu_cycles in total_cycles.items():
#     if thread_name in thread_info:
#         cpu_percent = thread_info[thread_name]
#         percentage = (cpu_cycles / 100) * cpu_percent
#         print(f"{thread_name}: {percentage} / {cpu_cycles} ({cpu_percent}%)")
