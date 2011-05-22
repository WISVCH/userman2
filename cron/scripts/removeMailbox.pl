#!/usr/bin/perl
use strict;
use Cyrus::IMAP::Admin;

my $crpassword  = `cat /etc/cyrus.secret`;
$crpassword =~ /(.*)/;
$crpassword = $1;

my $s_uid = $ARGV[0];
my $archivedir = $ARGV[1];

if (-d $archivedir && $s_uid) {
    my $mbxpath = `su cyrus -c '/usr/sbin/mbpath user.$s_uid'`;
    chop ($mbxpath);

    # Cyrus mail bewaren
    `tar czvf $archivedir/$s_uid-cyrus.tgz $mbxpath`;

    if ( -r "/var/mail/$s_uid" ) {
        # Inbox verwijderen
        `rm /var/mail/$s_uid`;
    }
    
#    system("kinit -t /etc/cyrus.keytab cyrus");

    # Cyrus mail verwijderen
    my $cyradm = Cyrus::IMAP::Admin->new('ch.tudelft.nl');
    $cyradm->authenticate(-user=>'cyrus', -password=>$crpassword);
#   $cyradm->authenticate(-user=>'cyrus');

    my $inboxname = "user.$s_uid";
    # Set ACL
    $cyradm->setaclmailbox($inboxname, 'cyrus', 'c');
    print STDERR "Error: ", $cyradm->error, "\n" if $cyradm->error;
    # Delete mailstore
    $cyradm->deletemailbox($inboxname);
    print STDERR "Error: ", $cyradm->error, "\n" if $cyradm->error;
    exit(0);
}

print STDERR "Error: Invalid command line options";
exit(1);
