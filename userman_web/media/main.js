function confirmpopup(text)
{
    if (text) {
	return confirm(text);    
    }
    else {
	return confirm('Weet je dat allemaal wel zeker?');
    }
}
