#include "FromPicture.h"
namespace robert {

    FromPicture::FromPicture () {}
    FromPicture::~FromPicture () {}

    FromPicture::FromPicture (const tesseract::Image src_pix) {

	l_int32    w;
	l_int32    h;
	l_int32    d;
//	, h, d;
	l_int32*   pw;
	l_int32*   ph;
	l_int32*   pd;
	//, ph, pd;
	pw = &w;
	ph = &h;
pd = &d;

	pixGetDimensions(src_pix, pw, ph, pd);
	printf("%d,%d,%d\nROBERT\n",w,h,d);
      	*pix = pixCreate(pixGetWidth(src_pix), pixGetHeight(src_pix), 1);
	pixWrite("gebinariseerd2.png", *pix, IFF_PNG);

	pixdata = pixGetData(*pix);
  	wpl = pixGetWpl(*pix);
  	src_wpl = pixGetWpl(src_pix);
  	srcdata = pixGetData(src_pix);
  	pixSetXRes(*pix, pixGetXRes(src_pix));
  	pixSetYRes(*pix, pixGetYRes(src_pix));
	num_channels = pixGetDepth(src_pix) / 8;
        _src_pix = src_pix;
    }
}
