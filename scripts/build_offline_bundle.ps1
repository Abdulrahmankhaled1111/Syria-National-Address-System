param(
  [string]$ReleaseTag = "0.18.0",
  [string]$OutputDirectory = "output/offline-release"
)
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$destination = Join-Path $root $OutputDirectory
New-Item -ItemType Directory -Force -Path $destination | Out-Null

docker build --pull=false -t "sna-offline:$ReleaseTag" $root
docker image inspect "nginx:1.27-alpine" | Out-Null
docker image inspect "postgis/postgis:16-3.4" | Out-Null
docker save -o (Join-Path $destination "container-images.tar") "sna-offline:$ReleaseTag" "nginx:1.27-alpine" "postgis/postgis:16-3.4"

$files = @(
  "docker-compose.offline.yml", "deploy/nginx.conf", "deploy/.env.offline.example",
  "scripts/install_offline.sh", "scripts/backup.sh", "scripts/restore.sh"
)
foreach ($relative in $files) {
  $target = Join-Path $destination $relative
  New-Item -ItemType Directory -Force -Path (Split-Path -Parent $target) | Out-Null
  Copy-Item -LiteralPath (Join-Path $root $relative) -Destination $target -Force
}
Copy-Item -LiteralPath (Join-Path $root "db") -Destination (Join-Path $destination "db") -Recurse -Force
Copy-Item -LiteralPath (Join-Path $root "docs/AIR_GAPPED_OPERATION.md") -Destination (Join-Path $destination "AIR_GAPPED_OPERATION.md") -Force

$manifest = Get-ChildItem -Path $destination -Recurse -File | Where-Object Name -ne "SHA256SUMS.txt" | ForEach-Object {
  $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $_.FullName).Hash.ToLowerInvariant()
  $relative = $_.FullName.Substring($destination.Length + 1).Replace("\", "/")
  "$hash  $relative"
}
Set-Content -LiteralPath (Join-Path $destination "SHA256SUMS.txt") -Value $manifest -Encoding ascii
Write-Host "Offline release created at $destination"
