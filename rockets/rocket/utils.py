
import hashlib 

def hashdict(obj):
	return hashlib.sha1(unicode(obj)).hexdigest()
