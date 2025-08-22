Output preview2.gif

Set Shell "bash"
Set FontSize 16
Set FontFamily "Cascadia Code"
Set WindowBar Colorful
Set LineHeight 1.6
Set Padding 15
Set Width 1050
Set Height 500
Set TypingSpeed 100ms

Require "taskly"

Type "taskly --help" Sleep 300ms Enter Sleep 3s
Type "taskly add 'Visit grandma'" Sleep 300ms Enter Sleep 700ms
Type "taskly add 'Finish CS50P'" Sleep 300ms Enter Sleep 700ms
Type "taskly add 'Read a book'" Sleep 300ms Enter Sleep 700ms
Type "taskly list" Sleep 300ms Enter Sleep 700ms
Type "taskly update 2 -d 'Finish CS50P project'" Sleep 300ms Enter Sleep 700ms
Type "taskly update 1 --description 'Visit grandma this weekend'" Sleep 300ms Enter Sleep 700ms
Type "taskly update 3 -s 'in-progress'" Sleep 300ms Enter Sleep 700ms
Type "taskly mark-done 1" Sleep 300ms Enter Sleep 700ms
Type "taskly mark-in-progress 2" Sleep 300ms Enter Sleep 700ms
Type "taskly list -s 'in-progress'" Sleep 300ms Enter Sleep 700ms
Type "taskly list --status 'done'" Sleep 300ms Enter Sleep 700ms
Type "taskly delete 3" Sleep 300ms Enter Sleep 700ms
Type "taskly list -d '>2024' # task added on or after 2024" Sleep 300ms Enter Sleep 700ms

Sleep 5s