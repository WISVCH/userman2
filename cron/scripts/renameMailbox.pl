#!/usr/bin/perl
use strict;
use Cyrus::IMAP::Admin;

exit 1;

my $s_olduid = $ARGV[0];
my $s_uid = $ARGV[1];

#my $crpassword 	= `cat /etc/cyrus.secret`;
my $crpassword 	= "dummy";
$crpassword =~ /(.*)/;
$crpassword = $1;

if ( $s_olduid && $s_uid ) {
	print "Should rename mailbox ($s_olduid) to ($s_uid)\n";

        # Cyrus mail verwijderen
        my $cyradm = Cyrus::IMAP::Admin->new('ch.chnet');
        $cyradm->authenticate(-user=>'cyrus', -password=>$crpassword);

        my $inboxname = "user.$s_olduid";
        my $newinboxname = "user.$s_uid";

        print "\t[ Set acl ]$inboxname\n";
        $cyradm->setaclmailbox($inboxname, 'cyrus', 'c');
        print STDERR "Error: ", $cyradm->error, "\n" if $cyradm->error;

        print "\t[ Rename mailstore ]$inboxname\n";
        $cyradm->renamemailbox($inboxname, $newinboxname);
        print STDERR "Error: ", $cyradm->error, "\n" if $cyradm->error;
	exit (0);
}

print STDERR "Error: invalid command line arguments\n";
