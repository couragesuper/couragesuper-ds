;d 키보드 메시지를 후킹하고, 메뉴 방식으로 실행하는 방법이 편리하여 사용.
; environment variables
	; := means assigned quetoed string
ScriptPath := "C:\Users\couragesuper\Desktop\shortcut.ahk"
BrowserPath := "C:\Program Files (x86)\Internet Explorer\iexplore.exe"
ChromePath := "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
ExpPath := "C:\Windows\explorer.exe"

; ShortCut List
; MsgBox , %ScriptPath%

ShortCut( var )
{
; MsgBox, %var%
}

OpenApp( var )
{
	; import global variables 
	global ChromePath 
	global ExpPath
	global BrowserPath
	
	;MsgBox, %var%
	if var = QT
	{
		Run , "C:\Qt\Qt5.12.0\Tools\QtCreator\bin\qtcreator.exe"
	}
	else if var = edit
	{
		Run , "C:\Program Files\EditPlus\editplus.exe"
	}
	else if var = notebook
	{
		run, %ChromePath% "http://mthx.cafe24.com:8888"
	}
	else if var = pycharm
	{
		run , "C:\Program Files\JetBrains\PyCharm Community Edition 2020.1.2\bin\pycharm64.exe"
	}
	else if var = ssh
	{
		run , "C:\Program Files (x86)\Mobatek\MobaXterm\MobaXterm.exe"
	}
	else if var = yes24
	{
		run , "C:\Program Files (x86)\YES24eBook\YES24eBook.exe"
	}
	else if var = dashboard
	{
		run, %ChromePath% "https://docs.google.com/spreadsheets/d/1iYUtLr3M1gbRwZh0rirKy2V4pc8Hy2TfererXx0aXMY/edit#gid=1785815396"
	}
	else if var = dashdev
	{
		run , %ChromePath%  "https://docs.google.com/spreadsheets/d/1uY3U6J6pVKp_-n9H-VAf8ptRowsoHmciY7lCJt5PKOY/edit#gid=0"
	}
	else if var = androidstudio
	{
		run, "C:\Program Files\Android\Android Studio\bin\studio64.exe"
	}
	else if var = anaconda
	{
		run, "%windir%\System32\cmd.exe" "/K" "C:\ProgramData\Anaconda3\Scripts\activate.bat" "C:\ProgramData\Anaconda3"
	}
	else if var = anaconda2
	{
		run, "%windir%\System32\cmd.exe" "/K" C:\ProgramData\Anaconda3\Scripts\activate.bat C:\Users\couragesuper\.conda\envs\pyTorch
	}
	else if var = toad
	{
		run, "C:\Program Files\Quest Software\Toad for MySQL Freeware 8.0\toad.exe"
	}		
	else if var = chrome
	{
		run, "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
	}
	else if var = paperspace
	{
		run , %ChromePath%  https://www.paperspace.com/
	}
	else if var = qtdesign
	{
		run , "C:\Users\couragesuper\.conda\envs\pytorch\Library\bin\designer.exe"
	}
	else if var = thxmemo
	{
		run , D:\workspace\PyCharm\PyTorch\couragesuper-ds\mthx\DatabaseUtil\bin\mthx_thx.exe , D:\workspace\PyCharm\PyTorch\couragesuper-ds\mthx\DatabaseUtil\bin
	}
	else if var = poem
	{
		run , D:\workspace\PyCharm\PyTorch\couragesuper-ds\mthx\DatabaseUtil\bin\mthx_poem_util.exe , D:\workspace\PyCharm\PyTorch\couragesuper-ds\mthx\DatabaseUtil\bin
	}


	else
	{
		MsgBox, "Error" , "That command isn't exist"
	}
	return
}

SendKeys( var )
{	
	if var = ep
	{
		Send {k}{a}{r}{i}{s}{m}{a}{*}{#}{`%}{&}{8}{4}
	}
	else if var = ad
	{
		send {1}{q}{2}{w}{3}{e}{4}{r}{!}{!}
	}
	else if var = nas
	{
		send {l}{g}{e}{1}{2}{3}{4}
	}
	else if var = id
	{
		send {c}{o}{u}{r}{a}{g}{e}{s}{u}{p}{e}{r}{.}{k}{i}{m}
	}
	else if var = x
	{
		send {x}{9}{8}{6}{4}{8}{2}
	}
	else if var = birth
	{
		send {1}{9}{8}{0}{0}{7}{0}{9}
	}
	else if var = certi
	{
		send {k}{a}{r}{i}{s}{m}{a}{*}{#}{`%}{&}{8}{4}
	}

	return
}


;Quick Link
#1:: ;프로그램
; if 문의 {}를 아래와 같이 줄을 써줘야 한다.
InputBox, iParam, Shourcut, Links to programs2
OpenApp( iParam )
;ShortCut( iParam )
return

#2:: ;툴
InputBox, iParam, Shourcut, Links to tools
;OpenTools( iParam )
SendKeys( iParam )
return

#0:: ;모드변경 Script
run %ScriptPath%
return

;여기서부터 환경을 변경.
;입력상자, 변수, 상자타이틀, 메시지출력
InputBox, iParam , Configuration, [1:edit this script]
if iParam = 0
{
MsgBox "Reloading AHK Files"
run %ScriptPath%
}
if iParam = 1
{
MsgBox "Reloading AHK Files"
}
return