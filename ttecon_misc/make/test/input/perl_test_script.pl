#! /usr/bin/perl
#! C:/Perl/bin/perl

$message = shift || "This is a test.\n";

my $outfile = "./output.txt";

&print_output;

sub print_output {
open(OUTFILE, ">$outfile");
print OUTFILE "$message";
close (OUTFILE);
print "Test script completed\n"
}