
#include "Tetragon.h"
#include "FromPicture.h"
namespace robert {

// Default constructor
    Tetragon::Tetragon () {}
    Tetragon::~Tetragon () {}

class Tetragon::SideBorders
{
    public:
    int left;
    int right;
    int y;
    SideBorders(int y, int l, int r) {
        this->y = y;
        this->left = l;
        this->right = r;
    }
};

class Tetragon::Threshold{
	public:
		int channel;
		int threshold;
		int mean;
	Threshold(int channel, int threshold, int mean){
		this->channel = channel;
		this->threshold = threshold;
		this->mean = mean;
	}
};


class Tetragon::Cornerpoint
{
public:
    int x;
    int y;
    float wdivh;

public:
    Cornerpoint(int x1, int y1)
    {
        this->x = x1;
        this->y = y1;
    }
    Cornerpoint();
};
struct Tetragon::CornerComparator
{
    bool operator()(const Cornerpoint &Cornerpoint1, const Cornerpoint &Cornerpoint2)
    {
        return (Cornerpoint1.wdivh < Cornerpoint2.wdivh);
    }
};
struct Tetragon::CornerpointverticalComparator
{
    bool operator()(const Cornerpoint &Cornerpoint1, const Cornerpoint &Cornerpoint2)
    {
        return (Cornerpoint1.y < Cornerpoint2.y) || (Cornerpoint1.x < Cornerpoint2.x);
    }
};
struct Tetragon::ChannelContrastComparator
{
    bool operator()(const Threshold& Contrast1 , const Threshold& Contrast2)
    {
        return abs(Contrast1.threshold - Contrast1.mean) > abs(Contrast2.threshold - Contrast2.mean);
    }
};
Tetragon::Tetragon(int x1,
             int y1,
             int x2,
             int y2,
             int x3,
             int y3,
             int x4,
             int y4)
    {

        lijst.push_back(Cornerpoint(x1, y1));
        lijst.push_back(Cornerpoint(x2, y2));
        lijst.push_back(Cornerpoint(x3, y3));
        lijst.push_back(Cornerpoint(x4, y4));
        lijst.sort(CornerpointverticalComparator());// Find highest and lowest coördinates.
        int xtop;
        int ytop;
        int wtop, htop;
        int ybottom;
        ybottom = lijst.back().y;
        xtop = lijst.front().x;
        ytop = lijst.front().y;
        for (auto &i : lijst)
        {
            wtop = i.x - xtop;
            htop = i.y - ytop;
            if (ytop != i.y)
                i.wdivh = wtop / (float)htop;
            else if (xtop == i.x) // dit is het eerste punt
                i.wdivh = -std::numeric_limits<float>::infinity();
            else // laatste punt staat even hoog als eerste punt.
                i.wdivh = std::numeric_limits<float>::infinity();
        }
        lijst.sort(CornerComparator());// order coördinates from top counterclockwise
        // for (auto const& i : lijst) 
        // if (i.wdivh == -std::numeric_limits<float>::infinity())
        // continue;//skip known first top record
        auto curLefti = lijst.begin();
        auto curRighti = lijst.rbegin();
        Cornerpoint *prevLeft,*prevRight;
        for (int y = ytop; y <= ybottom; y++)
        {
            if (curLefti->y == ytop)
            {
                if (curRighti->y == ytop)
                {
                    sideborders.push_back(SideBorders(y,curLefti->x, curRighti->x));
                     prevRight = curRighti.operator->();
                    ++curRighti;
                }
                else
                    sideborders.push_back(SideBorders(y,curLefti->x, curLefti->x));

                prevLeft = curLefti.operator->();
                ++curLefti;
            }
            else
            {
                while (curLefti->y < y)
                {
                    ++curLefti;
                    prevLeft = curLefti.operator->();
                }
                while (curRighti->y < y)
                {
                    ++curRighti;
                    prevRight = curRighti.operator->();
                }
                sideborders.push_back(SideBorders(y,
                    prevLeft->x + (y - prevLeft->y) * (curLefti->x - prevLeft->x) / (float) (curLefti->y - prevLeft->y),
                    prevRight->x + (y - prevRight->y) * (curRighti->x - prevRight->x) / (float) (curRighti->y - prevRight->y)));
            }
        }
    }
/// Threshold the rectangle, taking everything except the src_pix
/// from the class, using thresholds/hi_values to the output pix.
/// NOTE that num_channels is the size of the thresholds and hi_values
// arrays and also the bytes per pixel in src_pix.
void Tetragon::ThresholdTetragonToPix(robert::FromPicture fp1, int *bestchannel, int *threshold, int *mean) {
  for (auto const &sb : sideborders)
  {
    const l_uint32 *linedata = fp1.srcdata + sb.y * fp1.src_wpl;
    for (int x = sb.left; x < sb.right; ++x) {
      int pixel = GET_DATA_BYTE(linedata, x * fp1.num_channels + bestchannel[0]);
      uint32_t *pixline = fp1.pixdata + sb.y * fp1.wpl;
      bool white_result = true;
      if ((pixel > threshold[0]) != (threshold[0] < mean[0])) {
        white_result = false;
        break;
      }
      if (white_result) {
        CLEAR_DATA_BIT(pixline, x);
      } else {
        SET_DATA_BIT(pixline, x);
      }
    }
  }
  pixWrite("gebinariseerd.png", *fp1.pix, IFF_PNG);
}

// Computes the histogram for the given image tetragon, and the given
// single channel. Each channel is always one byte per pixel.
// Histogram is always a kHistogramSize(256) element array to count
// occurrences of each pixel value.
// returns bordermean.
int Tetragon::HistogramTetragon(robert::FromPicture fp1, int channel, int *histogram) {
  channel = tesseract::ClipToRange(channel, 0, fp1.num_channels - 1);
  int bordercount = 0;
  float bordersum = 0;
  memset(histogram, 0, sizeof(*histogram) * tesseract::kHistogramSize);

  for (auto const &sb : sideborders)
  {
    const l_uint32 *linedata = fp1.srcdata + sb.y * fp1.src_wpl;
    for (int x = sb.left; x < sb.right; ++x) {
      int pixel = GET_DATA_BYTE(linedata, x * fp1.num_channels + channel);
      ++histogram[pixel];
      if (x == sb.left|| x == sb.right){
        bordercount++;
        bordersum += pixel;
      }
    }
  }
  return bordersum / bordercount;
}

void Tetragon::OtsuThresholdTetragon(robert::FromPicture fp1, int *bestchannel, int *threshold, int *mean) {


  pixWrite("gebinariseerd3.png", (*(fp1.pix)), IFF_PNG);
  std::list<Threshold> thresholdsandmeans;
  int edgemean;
  for (int ch = 0; ch < fp1.num_channels; ++ch) {
    // Compute the histogram of the image rectangle.
    int histogram[tesseract::kHistogramSize];
    edgemean = HistogramTetragon(fp1, ch, histogram);
    int H;
    int best_omega_0;
    int best_t = tesseract::OtsuStats(histogram, &H, &best_omega_0);
    thresholdsandmeans.push_back(Threshold(ch, best_t, edgemean));
  }
  thresholdsandmeans.sort(ChannelContrastComparator());
  bestchannel[0]= thresholdsandmeans.front().channel;
  threshold[0]= thresholdsandmeans.front().threshold;
  mean[0]= thresholdsandmeans.front().mean;
  return;
}
}
