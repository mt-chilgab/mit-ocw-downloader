param([Parameter(Mandatory=$true)][String]$LectureCode,
      [Parameter(Mandatory=$true)][String]$LectureSeasonYear,
      [Parameter(Mandatory=$true)][Int32]$LectureNumbers)

$LectureSeasonYear -Match '[a-z, A-Z]{1}' > $null
$LectureSeason = $Matches[0].ToUpper()
$LectureSeasonYear -Match '[0-9]{1,4}' > $null
$LectureYear = [String]([Int32]$Matches[0] % 100)
$TotalLectureCode = "MIT"+$LectureCode.ToUpper()+$LectureSeason+$LectureYear

$pwd_ = $pwd
$dd = Read-Host "Where to download the files?"
cd $dd

if([String]::IsNullOrWhiteSpace($(Get-Command Invoke-WebRequest))){echo "Please acquire Invoke-WebRequest command and restart"}
else{
	$UriBase = "http://www.archive.org/download/"+$TotalLectureCode+"/"+$TotalLectureCode.Replace('.', '_')+"_lec"
	(1..$LectureNumbers) | ForEach-Object{	
		if($_ -ge 10){	
			$Uri = $UriBase+$_+"_300k.mp4"
			$File = $dd+"\Lecture_"+$_+".mp4"
		}
		else{
			$Uri = $UriBase+"0"+$_+"_300k.mp4"
			$File = $dd+"\Lecture_0"+$_+".mp4"
		}
		try {echo "Checking on Lecture $_"
		     $FileSize = (Invoke-WebRequest -Uri $Uri -Method Head).Headers.'Content-Length'
		     $Download = $true}
		catch [System.Net.WebException] {$Download = $false
						 "Returned WebException even after retries. Looks like no resource was found. Maybe no video lecture is available?`n"}
		catch {$Download = $true
		       "Unknown error occurred($($_ -replace '.$', '')), continuing...`n"}
		if(Test-Path -Path $File){$FileExistence = ([Int32]$FileSize -gt [Int32](Get-Item $File).length)} else{$FileExistence = $true}
		if($Download -and $FileExistence){
			echo "Downloading Lecture $_"
			try {Invoke-WebRequest -Uri $Uri -OutFile $File}
			catch [System.Net.WebException] {"Check your connection. This didn't happen just before!`n"}
			catch {"Unknown error occurred($($_ -replace '.$', '')), continuing...`n"}
		}
		echo "`n"
	}
}

cd $pwd_
