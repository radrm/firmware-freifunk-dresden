#!/bin/sh

export TITLE="Verwaltung > Allgemein > Kennwort"
. $DOCUMENT_ROOT/page-pre.sh ${0%/*}

cat<<EOM
<h2>$TITLE</h2>
<br>
<fieldset class="bubble">
<legend>Info</legend>
	Die Firmware ist eine Testversion. Daher sind noch unwichtige Funktionen nicht implementiert.<br>
	Diese Funktionen werden nach und nach eingebaut.
</fieldset>
EOM

. $DOCUMENT_ROOT/page-post.sh
