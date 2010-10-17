#!/usr/bin/perl
use strict;
use Cyrus::IMAP::Admin;

# Config settings.
#my $crpassword 	= `cat /etc/cyrus.secret`;
my $s_uid 	= $ARGV[0];

#
# Password strippen van enter
#
#$crpassword =~ /(.*)/;
#$crpassword = $1;

system("kinit -t /etc/cyrus.keytab cyrus");

my $cyradm = Cyrus::IMAP::Admin->new('ch.tudelft.nl');
$cyradm->authenticate(-user=>'cyrus');

#$cyradm->authenticate(-user=>'cyrus', -password=>$crpassword);

my $inboxname = "user.$s_uid";
print "\n[ Creating Inbox ]$inboxname\n";
$cyradm->createmailbox($inboxname);
if ($cyradm->error)
{
    print STDERR "Error: ", $cyradm->error, "\n";
    exit(1);
}
$cyradm->setquota("user.$s_uid", "STORAGE", "1048576");
if ($cyradm->error)
{
    print STDERR "Error: ", $cyradm->error, "\n";
    exit(1);
}
