#ifndef FROMPICTURE_H
#define FROMPICTURE_H

#include <list>
#include <limits>

#include <allheaders.h>
#include <cstring>
#include "helpers.h"

namespace robert {

	class FromPicture
	{
    	public:
	    	tesseract::Image _src_pix;
	    	int _num_channels;
	    	FromPicture();
	    	FromPicture(tesseract::Image src_pix, int num_channels);
	    	~FromPicture();
	};
}
#endif
