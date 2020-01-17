$path = "D:\scripts"+"\\"
$path2 = "C:\ProgramData\Miniconda3\Lib\site-packages\dat_extract" + "\\"

$file = "SBARC_Ship_Variable_Extraction.py"
$file2 = "Glider_Extraction.py"
$file3 = "CalCofi.py"
$file4 = "sound_speed.py"
$file5 = "Spect_Generate_time.py"
$file6 = "Normalize_Data.py"

$cmd = $path2 + $file  
$cmd2 = $path2 + $file2  
$cmd3 = $path + $file3  
$cmd4 = $path + $file4  
$cmd5 = $path + $file5
$cmd6 = $path + $file6

Start-Process python -ArgumentList $cmd -NoNewWindow -Wait
#Start-Process python -ArgumentList $cmd2 -NoNewWindow -Wait
Start-Process python -ArgumentList $cmd3 -NoNewWindow -Wait
Start-Process python -ArgumentList $cmd4 -NoNewWindow -Wait
Start-Process python -ArgumentList $cmd5 -NoNewWindow -Wait
Start-Process python -ArgumentList $cmd6 -NoNewWindow -Wait