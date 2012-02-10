#!/usr/bin/perl
use strict;
use Cyrus::IMAP::Admin;

# Config settings.
my $crpassword     = `cat /etc/cyrus.secret`;
my $s_uid     = $ARGV[0];

#
# Password strippen van enter
#
$crpassword =~ /(.*)/;
$crpassword = $1;

# Log in
my $cyradm = Cyrus::IMAP::Admin->new('ch.chnet');
$cyradm->authenticate(-user=>'cyrus', -password=>$crpassword);

# Get info
my $inboxname = "user.$s_uid";
my %info = $cyradm->getinfo($inboxname);
print STDERR "Error: ", $cyradm->error, "\n" if $cyradm->error;

foreach my $attrib (sort keys %info) {
    $attrib =~ /([^\/]*)$/;
    my $attrname = $1;
    if ($ARGV[1]) {
    if ($ARGV[1] eq $attrname) {
            print $info{$attrib};
    }
    } else {
    print "$inboxname ";
    print $attrname . ": ";
        print $info{$attrib} . "\n";
    }
}
