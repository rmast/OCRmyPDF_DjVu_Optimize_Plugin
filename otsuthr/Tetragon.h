#ifndef TETRAGON_H
#define TETRAGON_H

#include <list>
#include <limits>
#include <otsuthr.h>

#include <allheaders.h>
#include <cstring>
#include "helpers.h"
#include "FromPicture.h"

namespace robert {

class Tetragon
{
class	SideBorders;
class	Cornerpoint;
struct CornerComparator;
struct CornerpointverticalComparator;
std::list<Cornerpoint> lijst;
std::list<SideBorders> sideborders;
    public:
	    Tetragon();
	    ~Tetragon();
    Tetragon(int x1,
             int y1,
             int x2,
             int y2,
             int x3,
             int y3,
             int x4,
             int y4);
// Computes the histogram for the given image tetragon, and the given
// single channel. Each channel is always one byte per pixel.
// Histogram is always a kHistogramSize(256) element array to count
// occurrences of each pixel value.
// returns bordermean.
int HistogramTetragon(robert::FromPicture fp1, int channel, int *histogram);

void OtsuThresholdTetragon(robert::FromPicture fp1, std::vector<int> &thresholds, std::vector<int> &edgemean);
};
    // for (auto i = lijst.rbegin(); i != lijst.rend(); ++i)
    // };

    // class Readrecord {
    //     int x1;
    //     int y1;
    //     int x2;
    //     int y2;
    //     int x3;
    //     int y3;
    //     int x4;
    //     int y4;
         }
#endif

