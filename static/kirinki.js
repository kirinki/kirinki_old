/** This file is part of kirinki.
 
 kirinki is free software: you can redistribute it and/or modify it under the
 terms of the GNU Affero General Public License as published by the Free
 Software Foundation, either version 3 of the License, or (at your option) any
 later version.

 kirinki is distributed in the hope that it will be useful, but WITHOUT ANY
 WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
 A PARTICULAR PURPOSE.  See the GNU Addero General Public License for more
 details.

 You should have received a copy of the GNU Affero General Public License along
 with kirinki. If not, see <http://www.gnu.org/licenses/>.
*/

$(document).ready(function() {
    $('ul.hmenu li.userMenu').mouseover(
	function(event) {
	    $('ul.hmenu li.userMenu ul').css("display","block");
	}
    );

    $('ul.hmenu li').mouseleave(
	function(event) {
	    $('ul.hmenu li ul').css("display","none");
	}
    );

    $('div.col21').ready(
	function(event) {
	    if($('div.col21').height() < $('div.col1').height() ) {
		$('div.col21').css("height", $('div.col1').height());
	    }

	    if($('div.col21').height() < $('div.col22').height() ) {
		$('div.col21').css("height", $('div.col22').height());
	    }

	    if($('div.col21').height() > $('div.col22').height() ) {
		$('div.col22').css("height", $('div.col21').height());
	    }
	}
    );

    $('div.col22').ready(
	function(event) {
	    if($('div.col21').height() < $('div.col22').height() ) {
		$('div.col21').css("height", $('div.col22').height());
	    }

	    if($('div.col21').height() > $('div.col22').height() ) {
		$('div.col22').css("height", $('div.col21').height());
	    }
	}
    );

    $('#id_isVideo').click(
	function(event) {
	    if($('#id_isVideo').is(':checked')) {
		$('#id_srcIP').parent().parent().hide();
		$('#id_srcPort').parent().parent().hide();
		$('#id_srcMux').parent().parent().hide();
		$('#id_vStream').parent().parent().show();
	    } else {
		$('#id_srcIP').parent().parent().show();
		$('#id_srcPort').parent().parent().show();
		$('#id_srcMux').parent().parent().show();
		$('#id_vStream').parent().parent().hide();
	    }
	}
    );

    $('#id_isVideo').ready(
	function(event) {
	    if($('#id_isVideo').is(':checked')) {
		$('#id_srcIP').parent().parent().hide();
		$('#id_srcPort').parent().parent().hide();
		$('#id_srcMux').parent().parent().hide();
		$('#id_vStream').parent().parent().show();
	    } else {
		$('#id_srcIP').parent().parent().show();
		$('#id_srcPort').parent().parent().show();
		$('#id_srcMux').parent().parent().show();
		$('#id_vStream').parent().parent().hide();
	    }
	}
    );
});
