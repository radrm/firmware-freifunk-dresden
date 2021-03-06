#!/bin/sh

node=$(uci get ddmesh.system.node)
tmpmin=$(uci get ddmesh.system.tmp_min_node)
tmpmax=$(uci get ddmesh.system.tmp_max_node)
if [ $node -ge $tmpmin -a $node -le $tmpmax ]; then
# 	export NOMENU=1	
	export TITLE="Auto-Setup"

	. $DOCUMENT_ROOT/page-pre.sh ${0%/*}

#echo "<pre>";set;echo "/<pre>"

cat<<EOM
<h1>Auto-Setup</h1>
Diese Seite wird automatisch aufgerufen, wenn das erste Mal eine Freifunk Firmware auf den Router gespielt wurde.<br />
Der Router wird mit am h&auml;ufigsten verwendeten Einstellungen konfiguriert. Die Einstellungen k&ouml;nnen sp&auml;ter ge&auml;ndert werden.<br />
Bei Starten des Auto-Setups, wird nach einem Nutzernamen und Passwort gefragt. Wurden diese bisher nicht ge&auml;ndert, so lauten der
Nutzername "root" und das Passwort "Admin".<br />
Das Passwort sollte nach dem Durchlaufen des Autosetups ge&auml;ndert werden.<br /><br />
	<a href="/admin/autosetup.cgi">Starte Auto-Setup</a>
EOM

	. $DOCUMENT_ROOT/page-post.sh ${0%/*}

else #autosetup

	export TITLE="Verwaltung > Allgemein"
	. $DOCUMENT_ROOT/page-pre.sh ${0%/*}

	cat<<EOM
<h1>$TITLE</h1>
<br>
<fieldset class="bubble">
Willkommen zu den Verwaltungs-Seiten dieses
Access-Points. Sende Kommentare oder Korrekturvorschl&auml;ge zu dieser
Web-Oberfl&auml;che unter Angabe der Firmware-Version ($(cat /etc/version)) in das Dresdner Freifunk Forum.
</fieldset>

<NOSCRIPT><table BORDER="0" class="note">
<tr><td>F&uuml;r das automatische Laden der Startseiten beim <a href="firmware.cgi">Neustart</a>
wird JavaScript ben&ouml;tigt.</td></tr>
</table></NOSCRIPT>

<p><b>Tipp</b>: Dr&uuml;cke
<KBD style="text-decoration: blink;">[F1]</KBD> oder zeige mit der Maus
auf eines der Steuerungselemente, um kurze Hilfetexte einzublenden.</p>

<br>
<fieldset class="bubble">
<legend>Notwendige Einstellungen</legend>
<table>
<tr><th width="20">Status</th><th>Einstellung</th></tr>
<tr class="colortoggle1"><td>$(test -n "$(uci get ddmesh.contact.email)" && echo '<img alt="OK" src="../images/yes.png">' || echo '<img alt="Not OK" src="../images/no.png">')</td><td><a href="contact.cgi">Kontaktinfos</a>: E-Mail</td></tr>
<tr class="colortoggle2"><td>$(test -n "$(uci get ddmesh.contact.location)" && echo '<img alt="OK" src="../images/yes.png">' || echo '<img alt="Not OK" src="../images/no.png">')</td><td><a href="contact.cgi">Kontaktinfos</a>: Standort </td></tr>
<tr class="colortoggle1"><td>$(test -n "$(uci get ddmesh.gps.latitude)" && test -n "$(uci get ddmesh.gps.longitude)" && test -n "$(uci get ddmesh.gps.altitude)" && echo '<img alt="OK" src="../images/yes.png">' || echo '<img alt="Not OK" src="../images/no.png">')</td><td><a href="contact.cgi">Kontaktinfos</a>: GPS Koordinaten </td></tr>

</table>
</fieldset>

<br>
<fieldset class="bubble">
<legend>System Version</legend>
<table>
<tr class="colortoggle1"><th>Freifunk Version (Dresden)</th><td>$(cat /etc/version)</td></tr>
<tr class="colortoggle2"><th>Git Revision</th><td>$(cat /etc/built_info | sed -n '/revision/s#.*:##p')</td></tr>
<tr class="colortoggle1"><th>Built Datum</th><td>$(cat /etc/built_info | sed -n '/builtdate/s#[^:]*:##p')</td></tr>
$(cat /etc/openwrt_release | sed 's#\(.*\)="*\([^"]*\)"*#<tr class="colortoggle2"><th>\1</th><td>\2</td></tr>#')
</table>
</fieldset>

<br>
<fieldset class="bubble">
<legend>System Info</legend>
<table>
<tr class="colortoggle2"><th>Nameserver:</th><td colspan="5">$(grep nameserver /tmp/resolv.conf.auto | sed 's#nameserver##g')</td></tr>                              
<tr class="colortoggle2"><th>Ger&auml;telaufzeit:</th><td colspan="5">$(uptime)</td></tr>                                                                            
<tr class="colortoggle2"><th>System:</th><td colspan="5">$(cat /proc/cpuinfo | sed -n '/system type/s#system[ 	]*type[ 	]*:##p')</td></tr>                  
<tr class="colortoggle2"><th>Ger&auml;teinfo:</th><td colspan="5">$(cat /var/sysinfo/model) - $(cat /proc/cpuinfo | sed -n '/system type/s#.*:[ 	]*##p')</td></tr>   
<tr class="colortoggle2"><th>SSH Fingerprint (md5)</th><td colspan="5">$(dropbearkey -y -f /etc/dropbear/dropbear_rsa_host_key | sed -n '/Fingerprint/s#Fingerprint: md5 ##p')</td></tr>
<tr class="colortoggle1"><th></th><th>Total</th> <th>Used</th> <th>Free</th> <th>Shared</th> <th>Buffers</th> </tr>
$(free | sed -n '2,${s#[ 	]*\(.*\):[ 	]*\([0-9]\+\)[ 	]*\([0-9]\+\)[ 	]*\([0-9]*\)[ 	]*\([0-9]*\)[ 	]*\([0-9]*\)#<tr class="colortoggle2"><th>\1</th><td>\2</td><td>\2</td><td>\3</td><td>\4</td><td>\4</td></tr>#g;p}' )
</table>
</fieldset>
EOM

	cat<<EOM
<br>
<fieldset class="bubble">
<legend>DHCP Leases (aktuelle)</legend>
<table>
EOM

	IFS='
'
	T=1
	for i in $(cat /tmp/dhcp.leases | sed 's#\([^ ]\+\) \([^ ]\+\) \([^ ]\+\) \([^ ]\+\) \([^ ]\+\)#D="$(date --date=\"@\1\")";MAC1=\2;IP=\3;NAME=\4;MAC2=\5#')
	do
		eval $i
		echo "<tr class="colortoggle$T" ><th>Zeit:</th><td>$D</td><th>MAC:</th><td>$MAC1</td><th>IP:</th><td>$IP</td><th>Name:</th><td>$NAME</td></tr>"
		if [ $T = 1 ]; then T=2 ;else T=1; fi
	done

	cat<<EOM
</table>
</fieldset>
<br>
<fieldset class="bubble">
<legend>Internals</legend>
<table>
<tr><th></th><th>Vorhergehend</th><th>Aktuell</th></tr>
EOM

eval $(/usr/lib/ddmesh/ddmesh-overlay-md5sum.sh read | sed 's#\(.*\):\(.*\)$#ovl_\1=\2#')
if [ "$ovl_old" = "$ovl_cur" ]; then
 co="green"
else
 co="red"
fi

echo "<tr class=\"colortoggle1\" style=\"font-weight:bold;color: $co;\"><th>Overlay(md5sum)</th><td>$ovl_old</td><td>$ovl_cur</td></tr>"

cat<<EOM
</table>
</fieldset>
EOM

	. $DOCUMENT_ROOT/page-post.sh

fi #autosetup


