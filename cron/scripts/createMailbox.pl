#!/usr/bin/perl
use strict;
use Cyrus::IMAP::Admin;

exit 1;

# Config settings.
my $crpassword 	= `cat /etc/cyrus.secret`;
my $s_uid 	= $ARGV[0];

#
# Password strippen van enter
#
$crpassword =~ /(.*)/;
$crpassword = $1;

my $cyradm = Cyrus::IMAP::Admin->new('ch.chnet');
$cyradm->authenticate(-user=>'cyrus', -password=>$crpassword);
my $inboxname = "user.$s_uid";
print "\n[ Creating Inbox ]$inboxname\n";
$cyradm->createmailbox($inboxname);
print STDERR "Error: ", $cyradm->error, "\n" if $cyradm->error;
$cyradm->setquota("user.$s_uid", "STORAGE", "1048576");
print STDERR "Error: ", $cyradm->error, "\n" if $cyradm->error;
