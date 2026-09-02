$desktopPath = [Environment]::GetFolderPath('Desktop')
if (Test-Path $desktopPath) {
    $WshShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut("$desktopPath\A2Z DSA Vault.lnk")
    $Shortcut.TargetPath = "c:\Users\himan\Downloads\dustbin\index.html"
    $Shortcut.WorkingDirectory = "c:\Users\himan\Downloads\dustbin"
    $Shortcut.Description = "Personal A2Z DSA Tracker & Vault"
    $Shortcut.Save()
    Write-Host "Created shortcut at: $desktopPath\A2Z DSA Vault.lnk"
} else {
    Write-Host "Desktop folder not found at standard path."
}
