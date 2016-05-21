function validateForm() {
	debugger
    var x = document.forms["myForm"]["fname"].value;
    //if (x == null || x == "") {
		if (x) {
			body="Dear Shashank ,"
		window.location="mailto:shashank_verma0020@bistacloud.com?subject=hii&body="+body;
        //alert("Name must be filled out");
        return false;
    
    }
}
