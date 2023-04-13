# coding=utf-8
# Copyright (C) 2020-2021 PowerLZY.
# This file is part of Anno Sandbox - https://github.com/PowerLZY/Anno Sandbox


import sys
import os
sys.path.append("..")
from lib.anno sandbox.common.constants import anno sandbox_ROOT

from instance import Instance
from loader import Loader
from modules.detection.strings import Strings_ngram
from modules.processing.anno sandboxml import ML

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from pprint import pprint

# The first stage is to load the data from the directory holding all the JSONs
loader = Loader()
loader.load_binaries_dir("../sample_data/dict")

# Then we extract all the relevant information from the loaded samples.
simple_features_dict = loader.get_simple_features()
features_dict = loader.get_features()
features_strings = features_dict['66']["strings"]



"""
例子：
simple_features_dict['165']:{
    u'injection_runpe': u'Executed a process and injected code into it, probably while unpacking', 
    u'worm_renocide': u'Creates known Renocide Worm files, registry keys and/or mutexes', 
    u'pe_features': u'The executable has PE anomalies (could be a false positive)', 
    u'raises_exception': u'One or more processes crashed', 
    u'dumped_buffer': u'One or more potentially interesting buffers were extracted, these generally contain injected code, configuration data, etc.', 
    u'antisandbox_productid': u'Retrieves Windows ProductID, probably to fingerprint the sandbox',
    u'antivirus_virustotal': u'File has been identified by at least one AntiVirus on VirusTotal as malicious', 
    u'allocates_rwx': u'Allocates read-write-execute memory (usually to unpack itself)',
    u'packer_upx': u'The executable is compressed using UPX'
}
"""
labels_dict = loader.get_labels()

# Now that all the needed information are at hand we create a anno sandboxml Machine Learning instance
# and inject therein all these information.
# ml = ML(context="notebook")
ml = ML()
ml.load_simple_features(simple_features_dict)
ml.load_features(features_dict)
ml.load_labels(labels_dict)

# Once loaded into ML class the data is reformated into Pandas DataFrame object
# therefore it is easy to manipulate and use it with variety of machine learning algorithms.
simple_features = ml.simple_features
features = ml.features
labels = ml.labels

"""
{'packer': None, 'file_renamed': [], 'files_operations': 5, 'files_renamed': 0, 'Comments': None, 'files_deleted': 0, 'section_attrs': {u'.reloc': 4.563135239901142, u'.data': 5.714073993806871, u'.rdata': 6.335321668165209, u'.text': 6.723680694442286, u'.rsrc': 3.6143275609945746}, 'files_exists': 2, 'size': 180736, 'InternalName': u'dpapimig', 'regkey_written': [], 'file_copied': [], 'regkey_deleted': [], 'languages': [u'ENGLISH', u'ENGLISH_US'], 'mutex': None, 'dns': {}, 'files_opened': 0, 'file_read': [], 'LegalCopyright': u'\\xa9 Microsoft Corporation. All rights reserved.', 'udp': [u'192.168.57.255', u'239.255.255.250'], 'files_failed': 0, 'http': {}, 'api_stats': {u'LdrUnloadDll': 2, u'GetSystemMetrics': 1, u'NtAllocateVirtualMemory': 58, u'NtQuerySystemInformation': 2, u'GetSystemInfo': 1, u'CreateActCtxW': 1, u'NtUnmapViewOfSection': 2, u'LdrGetProcedureAddress': 10, u'MessageBoxTimeoutW': 1, u'SetUnhandledExceptionFilter': 2, u'LoadStringW': 2, u'GetFileAttributesW': 2, u'NtCreateFile': 5, u'NtClose': 17, u'GetSystemTimeAsFileTime': 3, u'RegOpenKeyExA': 4, u'NtDeviceIoControlFile': 6, u'NtTerminateProcess': 3, u'LdrGetDllHandle': 4, u'LdrLoadDll': 1, u'NtFreeVirtualMemory': 28}, 'timestamp': 1427745061, 'file_written': [], 'files_copied': 0, 'resource_attrs': {u'RT_GROUP_CURSOR': u'MS Windows cursor resource - 1 icon, 32x256, hotspot @1x1', u'RT_CURSOR': u'data', u'RT_VERSION': u'data'}, 'tcp': [], 'FileDescription': u'DPAPI Key Migration Wizard', 'dynamic_imports': [u'C:\\DOCUME~1\\ADMINI~1\\LOCALS~1\\Temp\\5b28c86d7e581e52328942b35ece0d0875585fbb4e29378666d1af5be7f56b46.dll'], 'OriginalFilename': u'dpapimig.exe', 'static_imports': {'count': 9, u'WTSAPI32.dll': [u'WTSQueryUserToken'], u'IPHLPAPI.DLL': [u'GetAdaptersInfo'], u'KERNEL32.dll': [u'GetModuleFileNameA', u'SetFileTime', u'GetFileAttributesW', u'FindFirstFileW', u'FindClose', u'FindNextFileW', u'GetFileTime', u'GetLastError', u'GetLocalTime', u'TerminateProcess', u'OpenProcess', u'Process32NextW', u'Process32FirstW', u'CreateToolhelp32Snapshot', u'DeleteFileW', u'GetNativeSystemInfo', u'GetComputerNameW', u'FileTimeToLocalFileTime', u'SetCurrentDirectoryW', u'GetCurrentDirectoryW', u'GetEnvironmentVariableW', u'SetEnvironmentVariableW', u'SetFilePointer', u'GetFileSize', u'GetDiskFreeSpaceExW', u'GetLogicalDrives', u'LoadLibraryW', u'CreateFileA', u'GetCurrentProcess', u'GetVolumeInformationW', u'GetDriveTypeW', u'Module32FirstW', u'GetProcessTimes', u'GetExitCodeProcess', u'WaitForSingleObject', u'Sleep', u'GetACP', u'GetTempFileNameW', u'GetTempPathW', u'GetTempFileNameA', u'CreateThread', u'ReleaseMutex', u'CreateMutexW', u'SetErrorMode', u'GetFileAttributesA', u'GetFullPathNameA', u'FileTimeToSystemTime', u'FindFirstFileA', u'FindNextFileA', u'SetEndOfFile', u'HeapReAlloc', u'SetFileAttributesW', u'WriteFile', u'GetModuleFileNameW', u'CreateFileW', u'ReadFile', u'MultiByteToWideChar', u'WideCharToMultiByte', u'LoadLibraryA', u'GetProcAddress', u'lstrlenA', u'lstrcpyA', u'GlobalAlloc', u'GetTickCount', u'GlobalFree', u'CreateProcessW', u'FlushFileBuffers', u'WriteConsoleW', u'SetStdHandle', u'GetProcessHeap', u'GetStringTypeW', u'LCMapStringW', u'HeapSize', u'GetCurrentProcessId', u'QueryPerformanceCounter', u'GetEnvironmentStringsW', u'FreeEnvironmentStringsW', u'DeleteCriticalSection', u'GetStartupInfoW', u'GetFileType', u'SetHandleCount', u'GetConsoleMode', u'GetConsoleCP', u'InitializeCriticalSectionAndSpinCount', u'LeaveCriticalSection', u'GetTempPathA', u'CloseHandle', u'EnterCriticalSection', u'HeapDestroy', u'HeapCreate', u'GetStdHandle', u'GetSystemTimeAsFileTime', u'HeapAlloc', u'MoveFileW', u'RtlUnwind', u'HeapFree', u'GetCurrentThreadId', u'DecodePointer', u'GetCommandLineA', u'UnhandledExceptionFilter', u'SetUnhandledExceptionFilter', u'IsDebuggerPresent', u'IsProcessorFeaturePresent', u'EncodePointer', u'TlsAlloc', u'TlsGetValue', u'TlsSetValue', u'TlsFree', u'InterlockedIncrement', u'GetModuleHandleW', u'SetLastError', u'InterlockedDecrement', u'RaiseException', u'GetCPInfo', u'GetOEMCP', u'IsValidCodePage', u'ExitProcess'], u'OLEAUT32.dll': [u'SystemTimeToVariantTime'], u'ADVAPI32.dll': [u'LookupPrivilegeValueA', u'RegisterServiceCtrlHandlerA', u'OpenProcessToken', u'DuplicateTokenEx', u'CreateProcessAsUserW', u'SetServiceStatus', u'GetUserNameW', u'RegQueryValueExW', u'AdjustTokenPrivileges', u'RegOpenKeyW', u'RegCloseKey'], u'SHLWAPI.dll': [u'StrTrimW'], u'WS2_32.dll': [u'__WSAFDIsSet', u'htons', u'shutdown', u'closesocket', u'htonl', u'connect', u'ioctlsocket', u'socket', u'inet_addr', u'setsockopt', u'WSAStartup', u'select', u'send'], u'USER32.dll': [u'wsprintfW'], u'USERENV.dll': [u'CreateEnvironmentBlock', u'DestroyEnvironmentBlock']}, 'magic_byte': u'PE32 executable (DLL) (GUI) Intel 80386, for MS Windows', 'processes': [u'lsass.exe', u'rundll32.exe'], 'CompanyName': u'Microsoft Corporation', 'files_written': 0, 'signed': False, 'ProductName': u'Microsoft\\xae Windows\\xae Operating System', 'file_deleted': [], 'files_read': 0, 'strings': [u'!This program cannot be run in DOS mode.', u'`.rdata', u'@.data', u'@.reloc', u'PQQQQQQf', u'VPj j ', u'] VWh\\', u'SSSVSR', u'G,VSPW', u')ND)NP', u"M8j8h8'", u'U,QPWR', u'QQSVWd', u'9} tK9}$uA9}(uA', u'9E vcP', u'9}$tB+', u'9u(vDVSj', u'9u v&V', u'URPQQh', u'^SSSSS', u'u)jAXf;', u'HHt$HHt', u't\x1f=MOC', u'Ht\x1fHu4j', u't*=RCC', u';7|G;p', u'tR99u2', u'<at,<rt"<wt', u'j@j ^V', u';t$,v-', u'UQPXY]Y[', u't"SS9] u', u'PPPPPPPP', u'PPPPPPPP', u'tCHt(Ht ', u'<+t"<-t', u'+t HHt', u'W(9W$u', u'tm9_ th9_$tc', u'Flf+Fp', u'D$(8D*', u'Nxf+Fd', u'|$ WUSV', u'D$$SUV', u'login.live.com', u'TPQBXODU', u'%s%s %s', u'RPCSvc', u' zip 1.01 Copyright 1998-2004 Gilles Vollant - http://www.winimage.com/zLibDll', u'1.2.7.f-hanba-win64-v1', u'bad allocation', u'FlsFree', u'FlsSetValue', u'FlsGetValue', u'FlsAlloc', u'Unknown exception', u'HH:mm:ss', u'dddd, MMMM dd, yyyy', u'MM/dd/yy', u'December', u'November', u'October', u'September', u'August', u'February', u'January', u'Saturday', u'Friday', u'Thursday', u'Wednesday', u'Tuesday', u'Monday', u'Sunday', u'\x1f !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~', u'CorExitProcess', u'(null)', u'`h````', u'xpxxxx', u'`h`hhh', u'xppwpp', u'bad exception', u'UTF-16LE', u'UNICODE', u'\x1f !"#$%&\'()*+,-./0123456789:;<=>?@abcdefghijklmnopqrstuvwxyz[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~', u'\x1f !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`ABCDEFGHIJKLMNOPQRSTUVWXYZ{|}~', u'GetProcessWindowStation', u'GetUserObjectInformationW', u'GetLastActivePopup', u'GetActiveWindow', u'MessageBoxW', u" Complete Object Locator'", u" Class Hierarchy Descriptor'", u" Base Class Array'", u' Base Class Descriptor at (', u" Type Descriptor'", u"`local static thread guard'", u"`managed vector copy constructor iterator'", u"`vector vbase copy constructor iterator'", u"`vector copy constructor iterator'", u"`dynamic atexit destructor for '", u"`dynamic initializer for '", u"`eh vector vbase copy constructor iterator'", u"`eh vector copy constructor iterator'", u"`managed vector destructor iterator'", u"`managed vector constructor iterator'", u"`placement delete[] closure'", u"`placement delete closure'", u"`omni callsig'", u' delete[]', u' new[]', u"`local vftable constructor closure'", u"`local vftable'", u"`udt returning'", u"`copy constructor closure'", u"`eh vector vbase constructor iterator'", u"`eh vector destructor iterator'", u"`eh vector constructor iterator'", u"`virtual displacement map'", u"`vector vbase constructor iterator'", u"`vector destructor iterator'", u"`vector constructor iterator'", u"`scalar deleting destructor'", u"`default constructor closure'", u"`vector deleting destructor'", u"`vbase destructor'", u"`string'", u"`local static guard'", u"`typeof'", u"`vcall'", u"`vbtable'", u"`vftable'", u'operator', u' delete', u'__unaligned', u'__restrict', u'__ptr64', u'__eabi', u'__clrcall', u'__fastcall', u'__thiscall', u'__stdcall', u'__pascal', u'__cdecl', u'__based(', u'1#QNAN', u'1#SNAN', u' deflate 1.2.7 Copyright 1995-2012 Jean-loup Gailly and Mark Adler ', u'Qkkbal', u"[-&LMb#{'", u'w+OQvr', u'IN\x1fSKyu', u')\\ZEo^m/', u'H*0"ZOW', u'mj>zjZ', u'IiGM>nw', u'ewh/?y', u'OZw3(?', u'V_:X1:', u'CloseHandle', u'CreateProcessW', u'GlobalFree', u'GetTickCount', u'GlobalAlloc', u'lstrcpyA', u'lstrlenA', u'GetProcAddress', u'LoadLibraryA', u'WideCharToMultiByte', u'MultiByteToWideChar', u'ReadFile', u'CreateFileW', u'GetModuleFileNameW', u'WriteFile', u'SetFileAttributesW', u'GetModuleFileNameA', u'SetFileTime', u'GetFileAttributesW', u'FindFirstFileW', u'FindClose', u'FindNextFileW', u'GetFileTime', u'GetLastError', u'GetLocalTime', u'TerminateProcess', u'OpenProcess', u'Process32NextW', u'Process32FirstW', u'CreateToolhelp32Snapshot', u'DeleteFileW', u'GetNativeSystemInfo', u'GetComputerNameW', u'FileTimeToLocalFileTime', u'SetCurrentDirectoryW', u'GetCurrentDirectoryW', u'GetEnvironmentVariableW', u'SetEnvironmentVariableW', u'SetFilePointer', u'GetFileSize', u'GetDiskFreeSpaceExW', u'GetLogicalDrives', u'LoadLibraryW', u'CreateFileA', u'GetCurrentProcess', u'GetVolumeInformationW', u'GetDriveTypeW', u'Module32FirstW', u'GetProcessTimes', u'GetExitCodeProcess', u'WaitForSingleObject', u'GetACP', u'GetTempFileNameW', u'GetTempPathW', u'GetTempFileNameA', u'GetTempPathA', u'CreateThread', u'ReleaseMutex', u'CreateMutexW', u'SetErrorMode', u'GetFileAttributesA', u'GetFullPathNameA', u'FileTimeToSystemTime', u'FindFirstFileA', u'FindNextFileA', u'KERNEL32.dll', u'wsprintfW', u'USER32.dll', u'RegCloseKey', u'RegOpenKeyW', u'AdjustTokenPrivileges', u'LookupPrivilegeValueA', u'RegQueryValueExW', u'GetUserNameW', u'SetServiceStatus', u'CreateProcessAsUserW', u'DuplicateTokenEx', u'OpenProcessToken', u'RegisterServiceCtrlHandlerA', u'ADVAPI32.dll', u'OLEAUT32.dll', u'DestroyEnvironmentBlock', u'CreateEnvironmentBlock', u'USERENV.dll', u'StrTrimW', u'SHLWAPI.dll', u'WS2_32.dll', u'GetAdaptersInfo', u'IPHLPAPI.DLL', u'WTSQueryUserToken', u'WTSAPI32.dll', u'GetSystemTimeAsFileTime', u'HeapAlloc', u'MoveFileW', u'RtlUnwind', u'HeapFree', u'GetCurrentThreadId', u'DecodePointer', u'GetCommandLineA', u'UnhandledExceptionFilter', u'SetUnhandledExceptionFilter', u'IsDebuggerPresent', u'IsProcessorFeaturePresent', u'EncodePointer', u'TlsAlloc', u'TlsGetValue', u'TlsSetValue', u'TlsFree', u'InterlockedIncrement', u'GetModuleHandleW', u'SetLastError', u'InterlockedDecrement', u'RaiseException', u'GetCPInfo', u'GetOEMCP', u'IsValidCodePage', u'ExitProcess', u'GetStdHandle', u'HeapCreate', u'HeapDestroy', u'EnterCriticalSection', u'LeaveCriticalSection', u'InitializeCriticalSectionAndSpinCount', u'GetConsoleCP', u'GetConsoleMode', u'SetHandleCount', u'GetFileType', u'GetStartupInfoW', u'DeleteCriticalSection', u'FreeEnvironmentStringsW', u'GetEnvironmentStringsW', u'QueryPerformanceCounter', u'GetCurrentProcessId', u'HeapSize', u'LCMapStringW', u'GetStringTypeW', u'SetStdHandle', u'WriteConsoleW', u'FlushFileBuffers', u'HeapReAlloc', u'SetEndOfFile', u'GetProcessHeap', u'ServerDll.dll', u'ServiceMain', u'VeriSign, Inc.1\x1f0', u'VeriSign Trust Network1;09', u'2Terms of use at https://www.verisign.com/rpa (c)061806', u'/VeriSign Class 3 Extended Validation SSL SGC CA0', u'120918000000Z', u'140919235959Z0', u'Washington1', u'Private Organization1', u'6004134851', u'980521', u'Washington1', u'Redmond1', u'1 Microsoft Way1', u'Microsoft Corporation1', u'Passport1', u'login.live.com0', u'g!+:4c', u'login.live.com0', u'-http://EVIntl-crl.verisign.com/EVIntl2006.crl0D', u'https://www.verisign.com/cps04', u'\x1fhttp://EVIntl-ocsp.verisign.com09', u'-http://EVIntl-aia.verisign.com/EVIntl2006.cer0', u'VeriSign, Inc.1\x1f0', u'VeriSign Trust Network1:08', u'1(c) 2006 VeriSign, Inc. - For authorized use only1E0C', u'<VeriSign Class 3 Public Primary Certification Authority - G50', u'061108000000Z', u'161107235959Z0', u'VeriSign, Inc.1\x1f0', u'VeriSign Trust Network1;09', u'2Terms of use at https://www.verisign.com/rpa (c)061806', u'/VeriSign Class 3 Extended Validation SSL SGC CA0', u'https://www.verisign.com/cps0=', u',http://EVSecure-crl.verisign.com/pca3-g5.crl0 ', u'[0Y0W0U', u'image/gif0!0\x1f0', u'#http://logo.verisign.com/vslogo.gif0)', u'Class3CA2048-1-480=', u'!http://EVSecure-ocsp.verisign.com0\x1f', u'(@w9nHrE1]k9', u'VeriSign, Inc.1705', u'.Class 3 Public Primary Certification Authority0', u'061108000000Z', u'211107235959Z0', u'VeriSign, Inc.1\x1f0', u'VeriSign Trust Network1:08', u'1(c) 2006 VeriSign, Inc. - For authorized use only1E0C', u'<VeriSign Class 3 Public Primary Certification Authority - G50', u' http://crl.verisign.com/pca3.crl0', u'https://www.verisign.com/cps0', u'[0Y0W0U', u'image/gif0!0\x1f0', u'#http://logo.verisign.com/vslogo.gif04', u'http://ocsp.verisign.com0', u'dBaD4t0', u'.?AVCZipper@@', u'.?AVbad_alloc@std@@', u'.?AVexception@std@@', u'.?AVtype_info@@', u'                          ', u'abcdefghijklmnopqrstuvwxyz', u'ABCDEFGHIJKLMNOPQRSTUVWXYZ', u'                          ', u'abcdefghijklmnopqrstuvwxyz', u'ABCDEFGHIJKLMNOPQRSTUVWXYZ', u'.?AVbad_exception@std@@', u'incompatible version', u'buffer error', u'insufficient memory', u'data error', u'stream error', u'file error', u'stream end', u'need dictionary', u'PADDINGXXPADDINGPADDINGXXPADDINGPADDINGXXPADDINGPADD', u'2U2d2m2t2', u'5+525M5', u'7#8-8o8', u':":2:B:j:', u'92:9:O:', u';*;4;<;j;', u'<"<3<^<', u'>5>Y>e>', u'0J1[1z1', u'233F3S3a3m3', u"4'404^4*:u:", u'=:>2?]?s?', u'!0[0o0', u'1&1@1Y1', u'3H3O3h3v3|3', u'4>5$:*:E:a:', u'40?0H0l0', u'1?1`1m1', u'1&2-2I2y2', u'4+444i4', u'5C5J5i5', u';#;);/;|;', u'<\x1f<7<z<', u'?@?F?y?', u'6&60666n677', u'9":/:n:', u':!;,;2;8;>;N;V;u;{;', u';*<U<\\<', u'=-=@=L=m=', u'2\x1f2B2~2', u'3(3Q3_3z3', u'6L7V7^7', u'8"8L8T8', u'8.9<9C9I9', u':::H:O:', u';\x1f<-<:<A<_=', u'8Q8o8w8', u':4:V:v:', u'>#>5>t>z>', u'>S?o?x?', u'0%0+0x0', u'1&10161<1B1H1M1V1]1g1m1s1', u'3;3b3n3', u':d;p;|;', u'g1777?', u'?"?(?.?4?:?', u'3)3O3m3t3x3|3', u'3R4]4x4', u'5 5$5(5,5v5|5', u'6<6T6[6c6h6l6p6', u'7J7P7T7X7\\7', u';$<*</<7<G<Q<W<k<', u'>&?+?1?5?;???E?I?O?S?X?^?b?h?l?r?v?|?', u'8=9C9U9h9', u'<!<(</<6<=<E<M<U<a<j<o<u<', u'Z0_0j0q0}0', u'1(1=1c1', u'3f3v3|3', u'4"4)4.464?4K4P4U4[4_4e4j4p4u4', u'5/5T6f6F7P7]7', u':V;c;i;', u'0&0?0I0\\0', u'3$3,343K3d3', u'9,979Q9\\9d9t9z9', u':0;H;R;m;u;{;', u'4L7P7T7X7\\7`7d7h7', u'4,575=5b5h5m5n6', u'8*898F8R8b8i8x8', u'9M9\\9e9', u';0<X<z<', u'=*=<=A=', u'0a0h0}0', u'5*636?6x6', u'677B7L7]7h7(999A9G9L9R9', u':T:`:o:t:', u':*<M<Z<f<n<v<', u'>\x1f>1>H>V>\\>', u'0I1l1~1', u':.:@:R:x:', u';,;>;P;', u';9=>=C=H=X=', u"> >'>,>3>8>F>", u'>>?M?\\?', u'0%0`0z0', u'0(0;0M0', u'4#4-4D4i4', u'9#:K:d:', u';!;*;j;|;', u'5n6b7j7', u'9;:A:O:', u'2-8O8c8v=', u'6%666B6[6d6v6', u'7"7+7?7K7d7m7', u'6T7X7\\7p7t7x7', u'5$5,545', u'6 6$6(6,6064686<6@6D6H6L6P6T6X6\\6`6d6h6l6p6t6x6|6', u'7 7$7(7,7074787<7@7D7H7L7P7T7X7', u'8(848@8L8', u'X8\\8`8d8h8l8p8t8x8|8', u'3 3(3@3D3\\3l3p3', u'4D4H4P4\\4|4', u'505P5p5', u'606<6X6d6', u'7 7(7,7D7H7X7|7', u'8 8$8,8@8\\8`8|8', u'9 9,9H9h9', u':(:4:P:l:p:', u'9 9$9(9,9094989<9@9D9H9L9P9T9X9\\9`9d9h9l9p9t9x9|9', u': :$:(:,:0:4:8:<:@:D:H:L:P:T:X:', u';(;,;0;4;8;<;@;D;H;L;P;T;X;\\;`;d;h;l;p;', u'jjjjjj', u'jjjjjj', u'%s\\*.*', u'%s\\%s\\', u'%sd.e%sc "%s > %s" 2>&1', u'%sd.e%sc "%s%s %s > %s" 2>&1', u'r /a /s', u'%s\\%X%d.%s', u'KERNEL32.DLL', u'HH:mm:ss', u'dddd, MMMM dd, yyyy', u'MM/dd/yy', u'December', u'November', u'October', u'September', u'August', u'February', u'January', u'Saturday', u'Friday', u'Thursday', u'Wednesday', u'Tuesday', u'Monday', u'Sunday', u'mscoree.dll', u'runtime error ', u'TLOSS error', u'SING error', u'DOMAIN error', u'- Attempt to use MSIL code from this assembly during native code initialization', u'This indicates a bug in your application. It is most likely the result of calling an MSIL-compiled (/clr) function from a native constructor or from DllMain.', u'- not enough space for locale information', u'- Attempt to initialize the CRT more than once.', u'This indicates a bug in your application.', u'- CRT not initialized', u'- unable to initialize heap', u'- not enough space for lowio initialization', u'- not enough space for stdio initialization', u'- pure virtual function call', u'- not enough space for _onexit/atexit table', u'- unable to open console device', u'- unexpected heap error', u'- unexpected multithread lock error', u'- not enough space for thread data', u'- abort() has been called', u'- not enough space for environment', u'- not enough space for arguments', u'- floating point support not loaded', u'Microsoft Visual C++ Runtime Library', u'<program name unknown>', u'Runtime Error!', u'Program: ', u'(null)', u'         (((((                  H', u'         h((((                  H', u'                                 H', u'WUSER32.DLL', u'CONOUT$', u'VS_VERSION_INFO', u'StringFileInfo', u'040904B0', u'CompanyName', u'Microsoft Corporation', u'FileDescription', u'DPAPI Key Migration Wizard', u'FileVersion', u'6.1.7600.16385 (win7_rtm.090713-1255)', u'InternalName', u'dpapimig', u'LegalCopyright', u' Microsoft Corporation. All rights reserved.', u'OriginalFilename', u'dpapimig.exe', u'ProductName', u'Microsoft', u' Windows', u' Operating System', u'ProductVersion', u'6.1.7600.16385', u'VarFileInfo', u'Translation']}

"""

