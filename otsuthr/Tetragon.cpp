
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
        lijst.sort(CornerpointverticalComparator());
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
        lijst.sort(CornerComparator());
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
// Computes the histogram for the given image tetragon, and the given
// single channel. Each channel is always one byte per pixel.
// Histogram is always a kHistogramSize(256) element array to count
// occurrences of each pixel value.
// returns bordermean.
int Tetragon::HistogramTetragon(robert::FromPicture fp1, int channel, int *histogram) {
  int num_channels = pixGetDepth(fp1._src_pix) / 8;
  channel = tesseract::ClipToRange(channel, 0, num_channels - 1);
  int bordercount = 0;
  float bordersum = 0;
  memset(histogram, 0, sizeof(*histogram) * tesseract::kHistogramSize);
  int src_wpl = pixGetWpl(fp1._src_pix);

  l_uint32 *srcdata = pixGetData(fp1._src_pix);
  for (auto const &sb : sideborders)
     {

    const l_uint32 *linedata = srcdata + sb.y * src_wpl;
    for (int x = sb.left; x < sb.right; ++x) {
      int pixel = GET_DATA_BYTE(linedata, x * num_channels + channel);
      ++histogram[pixel];
      if (x == sb.left|| x == sb.right){
        bordercount++;
        bordersum += pixel;
      }
    }
  }
  return bordersum / bordercount;
}

void Tetragon::OtsuThresholdTetragon(robert::FromPicture fp1, std::vector<int> &thresholds, std::vector<int> &edgemean) {

  thresholds.resize(fp1._num_channels);
  edgemean.resize(fp1._num_channels);
  
  for (int ch = 0; ch < fp1._num_channels; ++ch) {
    thresholds[ch] = -1;
    edgemean[ch] = -1;
    // Compute the histogram of the image rectangle.
    int histogram[tesseract::kHistogramSize];
    edgemean[ch] = HistogramTetragon(fp1, ch, histogram);
    int H;
    int best_omega_0;
    int best_t = tesseract::OtsuStats(histogram, &H, &best_omega_0);
    thresholds[ch] = best_t;
  }

  return;
}
}
