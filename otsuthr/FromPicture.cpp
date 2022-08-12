#include "FromPicture.h"
namespace robert {
	FromPicture::FromPicture () {}
	FromPicture::FromPicture(tesseract::Image src_pix, int num_channels)
	{_src_pix = src_pix;
	_num_channels = num_channels; }
	FromPicture::~FromPicture (){}

}
