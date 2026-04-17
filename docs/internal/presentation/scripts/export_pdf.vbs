Option Explicit

Dim fso, projectRoot, pptxPath, pdfPath
Dim objPPT, objPresentation

Set fso = CreateObject("Scripting.FileSystemObject")
projectRoot = fso.GetParentFolderName(WScript.ScriptFullName)
projectRoot = fso.GetParentFolderName(projectRoot)
projectRoot = fso.GetParentFolderName(projectRoot)
pptxPath = projectRoot & "\\docs\\internal\\presentation\\MinAn_1_4_Abschlusspraesentation.pptx"
pdfPath = projectRoot & "\\docs\\internal\\presentation\\MinAn_1_4_Abschlusspraesentation.pdf"

On Error Resume Next

Set objPPT = CreateObject("PowerPoint.Application")
If Err.Number <> 0 Then
    WScript.Echo "Fehler beim Start von PowerPoint: " & Err.Description
    WScript.Quit 1
End If

objPPT.Visible = False
Set objPresentation = objPPT.Presentations.Open(pptxPath, , , 1)
If Err.Number <> 0 Then
    WScript.Echo "Fehler beim Oeffnen der Praesentation: " & Err.Description
    objPPT.Quit
    WScript.Quit 1
End If

objPresentation.ExportAsFixedFormat pdfPath, 2, 1
If Err.Number <> 0 Then
    WScript.Echo "Fehler beim PDF-Export: " & Err.Description
    objPresentation.Close
    objPPT.Quit
    WScript.Quit 1
End If

objPresentation.Close
objPPT.Quit

WScript.Echo "Export abgeschlossen: " & pdfPath

