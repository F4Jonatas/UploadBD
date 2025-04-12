$filePath = "C:\Users\Enzo\Desktop\Ideia Helper\Backup para OneDrvie\script.spec"
$fileContent = Get-Content -Path $filePath -Raw

$uploadUrl = "https://graph.microsoft.com/v1.0/me/drive/root:/script.spec:/content"
$Token     = "47f91ed4-a9a4-4f50-bf9b-6d819bfabf44"

$headers = @{
    "Authorization" = "Bearer $Token"
    "Content-Type" = "application/octet-stream"
}

$response = Invoke-RestMethod -Uri $uploadUrl -Method Put -Headers $headers -Body $fileContent

if ($response.StatusCode -eq 200) {
    Write-Host "File uploaded successfully."
} else {
    Write-Host "Upload failed. Status code: $($response.StatusCode)"
}