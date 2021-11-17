$path = "J:\scripts"+"\\"
$path2 = "C:\ProgramData\Miniconda3\Lib\site-packages\dat_extract" + "\\"
$file = "test.py"
$file2 = "Glider_Extraction.py"
$file3 = "plumes.py"
$file4 = "test.py"

$cmd = $path + $file  # This line of code will create the concatenate the path and file
$cmd2 = $path2 + $file2  # This line of code will create the concatenate the path and file
$cmd3 = $path + $file3  # This line of code will create the concatenate the path and file
$cmd4 = $path + $file4  # This line of code will create the concatenate the path and file
Start-Process python -ArgumentList $cmd -NoNewWindow -Wait
Start-Process python -ArgumentList $cmd2 -NoNewWindow -Wait
Start-Process python -ArgumentList $cmd3 -NoNewWindow -Wait
Start-Process python -ArgumentList $cmd4 -NoNewWindow -Wait