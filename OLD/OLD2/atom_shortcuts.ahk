#SingleInstance, Force

^h::
send, {Left}
return

^k::
send, {Up}
return

^j::
send, {Down}
return

^l::
send, {Right}
return

/*
open anaconda env
run ipython
import os
os.system('title 1')
*/
!q::
If text_selected
{
Send, ^c
;ClipWait, 1
WinActivate, 1
Send, ^v
send, +{Enter}
send, +{Enter}
}
return

OnClipboardChange:
if(A_EventInfo=1)
{
text_selected := true
}
else
text_selected := false
return


/*
open anaconda env
go to folder
change title to 2
run python <script.py> once
*/
^o::
send, ^s
WinActivate, ahk_class ConsoleWindowClass ahk_exe cmd.exe
send, {Up}
send, {Enter}
return
