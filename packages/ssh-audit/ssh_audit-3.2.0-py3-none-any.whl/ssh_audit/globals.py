"""
   The MIT License (MIT)

   Copyright (C) 2017-2024 Joe Testa (jtesta@positronsecurity.com)

   Permission is hereby granted, free of charge, to any person obtaining a copy
   of this software and associated documentation files (the "Software"), to deal
   in the Software without restriction, including without limitation the rights
   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
   copies of the Software, and to permit persons to whom the Software is
   furnished to do so, subject to the following conditions:

   The above copyright notice and this permission notice shall be included in
   all copies or substantial portions of the Software.

   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
   THE SOFTWARE.
"""
# The version to display.
VERSION = 'v3.2.0'

# SSH software to impersonate
SSH_HEADER = 'SSH-{0}-OpenSSH_8.2'

# The URL to the Github issues tracker.
GITHUB_ISSUES_URL = 'https://github.com/jtesta/ssh-audit/issues'

# The man page.  Only filled in on Docker, PyPI, Snap, and Windows builds.

# True when installed from a Snap package, otherwise False.
SNAP_PACKAGE = False

# Error message when installed as a Snap package and a file access fails.
SNAP_PERMISSIONS_ERROR = 'Error while accessing file.  It appears that ssh-audit was installed as a Snap package.  In that case, there are two options:  1.) only try to read & write files in the $HOME/snap/ssh-audit/common/ directory, or 2.) grant permissions to read & write files in $HOME using the following command: "sudo snap connect ssh-audit:home :home"'
BUILTIN_MAN_PAGE = """
SSH-AUDIT(1)                General Commands Manual               SSH-AUDIT(1)

[1mNAME[m
       [1mssh-audit[m - SSH server & client configuration auditor

[1mSYNOPSIS[m
       [1mssh-audit[m [[4moptions[24m] [4m<target_host>[24m

[1mDESCRIPTION[m
       [1mssh-audit[m  analyzes  the  configuration  of SSH servers & clients, then
       warns the user of weak, obsolete, and/or untested cryptographic  primi-
       tives.   It  is very useful for hardening SSH tunnels, which by default
       tend to be optimized for compatibility, not security.

       See <https://www.ssh-audit.com/> for official hardening guides for com-
       mon platforms.

[1mOPTIONS[m
       [1m-h,[m [1m--help[m
              Print short summary of options.

       [1m-1,[m [1m--ssh1[m
              Only perform an audit using SSH protocol version 1.

       [1m-2,[m [1m--ssh2[m
              Only perform an audit using SSH protocol version 2.

       [1m-4,[m [1m--ipv4[m
              Prioritize the usage of IPv4.

       [1m-6,[m [1m--ipv6[m
              Prioritize the usage of IPv6.

       [1m-b,[m [1m--batch[m
              Enables grepable output.

       [1m-c,[m [1m--client-audit[m
              Starts a server on port 2222 to audit client software configura-
              tion.   Use  -p/--port=<port>  to  change  port  and  -t/--time-
              out=<secs> to change listen timeout.

       [1m--conn-rate-test=N[:max[m[4m_[24m[1mrate][m
              Performs  a  connection rate test (useful for collecting metrics
              related   to   susceptibility   of   the   DHEat   vulnerability
              [CVE-2002-20001]).   A successful connection is counted when the
              server returns a valid SSH banner.  Testing is conducted with  N
              concurrent  sockets with an optional maximum rate of connections
              per second.

       [1m-d,[m [1m--debug[m
              Enable debug output.

       [1m--dheat=N[:kex[:e[m[4m_[24m[1mlen]][m
              Run the DHEat DoS attack  (CVE-2002-20001)  against  the  target
              server  (which  will  consume all available CPU resources).  The
              number of concurrent sockets, N, needed to achieve  this  effect
              will  be  highly dependent on the CPU resources available on the
              target, as well as the latency between the source and target ma-
              chines.  The key exchange is automatically chosen based on which
              would cause maximum effect, unless explicitly chosen in the sec-
              ond  field.   Lastly, an (experimental) option allows the length
              in bytes of the fake e value sent to the server to be  specified
              in  the  third  field.  Normally, the length of e is roughly the
              length of the modulus of the Diffie-Hellman exchange (hence,  an
              8192-bit  / 1024-byte value of e is sent in each connection when
              targeting  the  diffie-hellman-group18-sha512  algorithm).   In-
              stead,  it  was  observed  that  many SSH implementations accept
              small values, such as 4 bytes; this results in a much more  net-
              work-efficient attack.

       [1m-g,[m  [1m--gex-test=<x[,y,...][m [1m|[m [1mmin1:pref1:max1[,min2:pref2:max2,...][m [1m|[m [1mx-[m
       [1my[:step]>[m
              Runs a Diffie-Hellman Group Exchange modulus size test against a
              server.

              Diffie-Hellman requires the client and server to agree on a gen-
              erator value and a modulus value.  In the "Group  Exchange"  im-
              plementation of Diffie-Hellman, the client specifies the size of
              the modulus in bits by providing the server with  minimum,  pre-
              ferred  and  maximum  values. The server then finds a group that
              best matches the client's request, returning  the  corresponding
              generator  and  modulus.  For a full explanation of this process
              see RFC 4419 and its successors.

              This test acts as a client by providing an SSH server  with  the
              size  of  a modulus and then obtains the size of the modulus re-
              turned by the server.

              Three types of syntax are supported:

                1. <x[,y,...]>

                   A comma delimited list of modulus sizes.
                   A test is performed against each value in the list where it
              acts as the minimum, preferred and maximum modulus size.

                2. <min:pref:max[,min:pref:max,...]>

                   A  set  of  three  colon delimited values denoting minimum,
              preferred and maximum modulus size.
                   A test is performed against each set.
                   Multiple sets can specified as a comma separated list.

                3. <x-y[:step]>

                   A range of modulus sizes with an optional step value.  Step
              defaults to 1 if omitted.
                   If the left value is greater than the right value, then the
              sequence operates from right to left.
                   A test is performed against each value in the  range  where
              it acts as the minimum, preferred and maximum modulus size.

              Duplicates are excluded from the return value.

       [1m-j,[m [1m--json[m
              Output  results  in  JSON format.  Specify twice (-jj) to enable
              indent printing (useful for debugging).

       [1m-l,[m [1m--level=<info|warn|fail>[m
              Specify the minimum output level.  Default is info.

       [1m-L,[m [1m--list-policies[m
              List all official, built-in policies for common systems.   Their
              full  names  can then be passed to -P/--policy.  Add -v to -L to
              view policy change logs.

       [1m--lookup=<alg1,alg2,...>[m
              Look up the security information of an algorithm(s) in  the  in-
              ternal database.  Does not connect to a server.

       [1m-m,[m [1m--manual[m
              Print  the  man  page  (Docker,  PyPI,  Snap, and Windows builds
              only).

       [1m-M,[m [1m--make-policy=<custom[m[4m_[24m[1mpolicy.txt>[m
              Creates a policy based on the target server.  Useful when  other
              servers should be compared to the target server's custom config-
              uration (i.e.: a cluster environment).  Note that the  resulting
              policy can be edited manually.

       [1m-n,[m [1m--no-colors[m
              Disable color output.  Automatically set when the NO_COLOR envi-
              ronment variable is set.

       [1m-p,[m [1m--port=<port>[m
              The TCP port to connect to when auditing a server, or  the  port
              to listen on when auditing a client.

       [1m-P,[m [1m--policy=<"built-in[m [1mpolicy[m [1mname"[m [1m|[m [1mpath/to/custom[m[4m_[24m[1mpolicy.txt>[m
              Runs  a policy audit against a target using the specified policy
              (see [1mPOLICY[m [1mAUDIT[m section for detailed description of this  mode
              of operation).  Combine with -c/--client-audit to audit a client
              configuration instead of a server.   Use  -L/--list-policies  to
              list all official, built-in policies for common systems.

       [1m--skip-rate-test[m
              Skips  the  connection rate test during standard audits.  By de-
              fault, a few dozen TCP connections are created with  the  target
              host  to  see  if connection throttling is implemented (this can
              safely infer whether the target is vulnerable to the  DHEat  at-
              tack; see CVE-2002-20001).

       [1m-t,[m [1m--timeout=<secs>[m
              The  timeout,  in  seconds, for creating connections and reading
              data from the socket.  Default is 5.

       [1m-T,[m [1m--targets=<hosts.txt>[m
              A file containing a list of target hosts.  Each line  must  have
              one  host,  in the format of HOST[:PORT].  Use --threads to con-
              trol concurrent scans.

       [1m--threads=<threads>[m
              The number of threads to  use  when  scanning  multiple  targets
              (with -T/--targets).  Default is 32.

       [1m-v,[m [1m--verbose[m
              Enable verbose output.

[1mSTANDARD[m [1mAUDIT[m
       By  default,  [1mssh-audit[m performs a standard audit.  That is, it enumer-
       ates all host key types, key exchanges, ciphers, MACs, and other infor-
       mation,  then  color-codes  them  in output to the user.  Cryptographic
       primitives with potential issues are displayed  in  yellow;  primitives
       with serious flaws are displayed in red.

[1mPOLICY[m [1mAUDIT[m
       When the -P/--policy option is used, [1mssh-audit[m performs a policy audit.
       The target's host key types, key exchanges, ciphers,  MACs,  and  other
       information  is  compared  to  a  set of expected values defined in the
       specified policy file.  If everything matches,  only  a  short  message
       stating a passing result is reported.  Otherwise, the field(s) that did
       not match are reported.

       Policy auditing is helpful for ensuring a group of related servers  are
       properly hardened to an exact specification.

       The  set  of  official  built-in policies can be viewed with -L/--list-
       policies.    Multiple   servers   can   be   audited   with   -T/--tar-
       gets=<servers.txt>.   Custom  policies can be made from an ideal target
       server with -M/--make-policy=<custom_policy.txt>.

[1mEXAMPLES[m
       Basic server auditing:
              ssh-audit localhost
              ssh-audit 127.0.0.1
              ssh-audit 127.0.0.1:222
              ssh-audit ::1
              ssh-audit [::1]:222

       To run a standard  audit  against  many  servers  (place  targets  into
       servers.txt, one on each line in the format of HOST[:PORT]):
              ssh-audit -T servers.txt

       To  audit a client configuration (listens on port 2222 by default; con-
       nect using "ssh -p 2222 anything@localhost"):
              ssh-audit -c

       To audit a client configuration, with a listener on port 4567:
              ssh-audit -c -p 4567

       To list all official built-in policies (hint: use their full names with
       -P/--policy):
              ssh-audit -L

       To  run  a  built-in policy audit against a server (hint: use -L to see
       list of built-in policies):
              ssh-audit -P "Hardened Ubuntu Server 20.04 LTS (version 1)" targetserver

       To run a custom policy audit against a server (hint: use -M/--make-pol-
       icy to create a custom policy file):
              ssh-audit -P path/to/server_policy.txt targetserver

       To run a policy audit against a client:
              ssh-audit -c -P ["policy name" | path/to/client_policy.txt]

       To run a policy audit against many servers:
              ssh-audit -T servers.txt -P ["policy name" | path/to/server_policy.txt]

       To  create  a  policy  based  on a target server (which can be manually
       edited; see official built-in policies for syntax examples):
              ssh-audit -M new_policy.txt targetserver

       To run a Diffie-Hellman Group Exchange modulus size test using the val-
       ues 2000 bits, 3000 bits, 4000 bits and 5000 bits:
              ssh-audit targetserver --gex-test=2000,3000,4000,5000

       To  run  a  Diffie-Hellman  Group Exchange modulus size test where 2048
       bits is the minimum, 3072 bits is the preferred and 5000  bits  is  the
       maximum:
              ssh-audit targetserver --gex-test=2048:3072:5000

       To run a Diffie-Hellman Group Exchange modulus size test from 0 bits to
       5120 bits in increments of 1024 bits:
              ssh-audit targetserver --gex-test=0-5120:1024

       To run the DHEat DoS attack (monitor the target server's CPU  usage  to
       determine the optimal number of concurrent sockets):
              ssh-audit targetserver --dheat=10

       To  run  the DHEat attack and manually target the diffie-hellman-group-
       exchange-sha256 algorithm:
              ssh-audit targetserver --dheat=10:diffie-hellman-group-exchange-sha256

       To run the DHEat attack and manually target  the  diffie-hellman-group-
       exchange-sha256  algorithm  with a very small length of e (resulting in
       the same effect but without having to send large packets):
              ssh-audit targetserver --dheat=10:diffie-hellman-group-exchange-sha256:4

       To test the number of successful connections per  second  that  can  be
       created  with the target using 8 parallel threads (useful for detecting
       whether connection throttling is implemented by the target):
              ssh-audit targetserver --conn-rate-test=8

       To use 8 parallel threads to create up to 100  connections  per  second
       with  the  target (useful for understanding how much CPU load is caused
       on the target simply from handling new connections  vs  excess  modular
       exponentiation when performing the DHEat attack):
              ssh-audit targetserver --conn-rate-test=8:100

[1mRETURN[m [1mVALUES[m
       When  a  successful  connection is made and all algorithms are rated as
       "good", [1mssh-audit[m returns 0.  Other possible return values are:

              1 = connection error
              2 = at least one algorithm warning was found
              3 = at least one algorithm failure was found
              <any other non-zero value> = unknown error

[1mSSH[m [1mHARDENING[m [1mGUIDES[m
       Hardening   guides   for   common   platforms   can   be   found    at:
       <https://www.ssh-audit.com/>

[1mBUG[m [1mREPORTS[m
       Please     file     bug    reports    as    a    Github    Issue    at:
       <https://github.com/jtesta/ssh-audit/issues>

[1mAUTHOR[m
       [1mssh-audit[m was originally written by Andris Raugulis  <moo@arthepsy.eu>,
       and maintained from 2015 to 2017.

       Maintainership  was  assumed and development was resumed in 2017 by Joe
       Testa <jtesta@positronsecurity.com>.

                                April 18, 2024                    SSH-AUDIT(1)
"""
