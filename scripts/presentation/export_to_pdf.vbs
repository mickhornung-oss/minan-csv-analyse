Option Explicit

Dim fso, projectRoot, pptxPath, pdfPath
Dim objPPT, objPresentation

Set fso = CreateObject("Scripting.FileSystemObject")
projectRoot = fso.GetParentFolderName(WScript.ScriptFullName)
projectRoot = fso.GetParentFolderName(projectRoot)
projectRoot = fso.GetParentFolderName(projectRoot)
pptxPath = projectRoot & "\presentation\MinAn_1_4_Abschlusspraesentation.pptx"
pdfPath = projectRoot & "\presentation\MinAn_1_4_Abschlusspraesentation.pdf"

Set objPPT = CreateObject("PowerPoint.Application")
objPPT.Visible = True
Set objPresentation = objPPT.Presentations.Open(pptxPath)
objPresentation.ExportAsFixedFormat pdfPath, 2
objPresentation.Close
objPPT.Quit
Set objPPT = Nothing
