#ifndef FROMPICTURE_H
#define FROMPICTURE_H

#include <list>
#include <limits>
#include <otsuthr.h>
#include <allheaders.h>
#include <cstring>
#include "helpers.h"

namespace robert {

	class FromPicture
	{
    		public:
			tesseract::Image *pix;
    			uint32_t *pixdata;
    			int wpl;
    			int src_wpl;
    			uint32_t *srcdata;
    			int num_channels;
    			tesseract::Image _src_pix;
    			FromPicture();
    			FromPicture(tesseract::Image src_pix);
    			~FromPicture();
	};
}
#endif

