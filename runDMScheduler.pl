#!/usr/bin/perl

use strict; 
use warnings; 
use MIME::Lite; 

use Win32::Process;
use Win32;
use Date::Calc qw(Add_Delta_Days);
use Date::Calc qw(Delta_Days);
use Sys::Hostname;



	my @f = (localtime)[3..5]; # grabs day/month/year values
	my @now_date = ($f[2] + 1900, $f[1] +1, $f[0]);

	my $year;
	my $month;
	my $day;

	($year, $month, $day) = @now_date;
	my $date = sprintf "%04d%02d%02d", $year, $month, $day;

my $logfile = "logs/DMS_raw_".$date.".LOG";


system("C:/Python34/python.exe runDatamix_Scheduler.py > $logfile");




###-----



my $body = "";
my $result = "";
# --------------------------------------------------------------------

open FILE, $logfile or $body = "Couldn't open file: $!"; 
while (<FILE>){
	$body .= $_;
#	if (/RESTORE DATABASE/) {
#		$result .= "RESTORE DB " . substr($_,16,45); # <$'>: the Right part of the match
#	}
}
close FILE;


# --------------------------------------------------------------------

my $msg = MIME::Lite->new( 
        From        =>  'datamixalerts@acme.com',
        To          =>  'datamixalerts@acme.com', 
        Subject     =>  "DatamixV2: rawScheOut-".$date, 
		Type     	=>  'text',
		Data     	=>  $body
	); 

$msg->send('smtp', 'lwpsync01', Timeout => 600 ); 

# --------------------------------------------------------------------

	