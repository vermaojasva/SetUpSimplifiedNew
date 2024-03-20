#Define an array of chocolatey installation commands
$softwarestoInstall = $args

Write-Host "Softwares to install are: $softwaresToInstall"

choco install $softwaresToInstall -y

pause

Write-Host "All installations completed."