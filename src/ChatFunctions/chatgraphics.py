import numpy as np
import datetime
import matplotlib.pyplot as plt
from misc.classes import Chat, Member, MediaType
from misc.keywords import LANGUAGES, GRAPHIC_KEYWORDS

# Exclusive for the radar_factory internal usage
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections import register_projection
from matplotlib.projections.polar import PolarAxes
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D



#! For testing, only. Uncomment when testing 
#from ChatFunctions.chatparser import parseChat
### Your parsed message chat, here.
#from ChatFunctions.chatnalisis import getTimeDicts


### Pies

def makeMessagePie(gc: Chat, langage:str="SPANISH"):
    # plt.style.use('_mpl-gallery')
    x = []
    labels = []
    for member in list(gc.members.values()):
        if member.m_ammount:
            x.append(member.m_ammount)
            labels.append(member.name)

    # colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, len(x)))

    # plot
    fig, ax = plt.subplots()
    ax.pie(x, labels=labels, radius=3, center=(4, 4),
           wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=False)
    
    # ax.legend(loc="upper left")

    ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
           ylim=(0, 8), yticks=np.arange(1, 8))
    ax.set_axis_off()
    plt.savefig("internal/messagePie.svg",transparent=False)
    plt.close()

def mediaSentByChatter(gc: Chat, language:str="SPANISH"):
    for member in list(gc.members.values()):
        x = []
        labels = []
        for m_type in MediaType:
            if member.mediaSent.get(m_type,0):
                x.append(member.mediaSent[m_type])
                # x[0] -= member.mediaSent[m_type]
                labels.append(m_type.value)
        
        if x and labels:
            fig, ax = plt.subplots()
            ax.pie(x, labels=labels, labeldistance=None, radius=3, center=(4, 4), wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=False)
    
            ax.legend(loc="upper left")

            ax.set_title(member.name)

            ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
                ylim=(0, 8), yticks=np.arange(1, 8))
            ax.set_axis_off()
            plt.savefig(f"internal/{member.name}-mediaSent.svg",transparent=False)
            # plt.show()
            plt.close()

### Time stackplots

def makeTimeStackplot(gc:Chat, language:str="SPANISH"):
    listsPerChatter:dict[str, tuple[list[datetime.date],list[int]]] = {} # name : [(date, number of messages)]
    for member in list(gc.members.values()):
        dateList = []
        messageCount = []
        member.messages.sort(key=lambda x:x.dtime) #Just in case! This should not matter
        for message in member.messages:
            date = message.dtime
            if date.date() in dateList:
                messageCount[-1] += 1
            else:
                dateList.append(date.date())
                messageCount.append(0)
        if (dateList and messageCount): listsPerChatter[member.name] = [dateList, messageCount]


    for chatter, lists in listsPerChatter.items():
        fig, ax = plt.subplots()
        x, y = lists
        start = x[0]
        end = x[-1]
        time = np.arange(start, end, dtype='datetime64[D]')
        extended_y = []
        for date in time:
            if x[0] == date:
                extended_y.append(y[0])
                y = y[1:]
                x = x[1:]
            else:
                extended_y.append(0)
        ax.plot(time, extended_y)
        ax.set_title(chatter)
        plt.tight_layout()
        ax.tick_params(axis='both', which='major', labelsize=8)
        plt.savefig(f"internal/{chatter}-time-stackplot.svg",transparent=False)

    start = listsPerChatter[min(listsPerChatter, key=lambda x: listsPerChatter.get(x)[0][0])][0][0]
    end = listsPerChatter[max(listsPerChatter, key=lambda x: listsPerChatter.get(x)[0][-1])][0][-1]

    time = np.arange(start, end, dtype='datetime64[D]')
    extendedMessageCount = {}
    for date in time:
        for chatter, lists in listsPerChatter.items():
            if chatter not in extendedMessageCount.keys(): extendedMessageCount[chatter] = []
            if lists[0] and lists[0][0] == date:
                extendedMessageCount[chatter].append(lists[1][0] + 1) # See below for the reason of the +1
                lists[0] = lists[0][1:]
                lists[1] = lists[1][1:]
            else:
                extendedMessageCount[chatter].append(1) # Technically incorrect, but if the value is zero then a line is not drawn and the result is ugly. This means all graphics are off by 1.
    y = np.vstack([v for v in extendedMessageCount.values()])
    fig, ax = plt.subplots()
    ax.stackplot(time, y, labels=extendedMessageCount.keys())
    ax.legend(loc='upper left')
    ax.tick_params(axis='both', which='major', labelsize=8)
    plt.tight_layout()
    plt.savefig("internal/total-time-stackplot.svg",transparent=False)
    plt.close()

## Internal function, from Matplotlib's official site.
def radar_factory(num_vars, frame='circle'):
    """
    Create a radar chart with `num_vars` Axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle', 'polygon'}
        Shape of frame surrounding Axes.

    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)

    class RadarTransform(PolarAxes.PolarTransform):

        def transform_path_non_affine(self, path):
            # Paths with non-unit interpolation steps correspond to gridlines,
            # in which case we force interpolation (to defeat PolarTransform's
            # autoconversion to circular arcs).
            if path._interpolation_steps > 1:
                path = path.interpolated(num_vars)
            return Path(self.transform(path.vertices), path.codes)

    class RadarAxes(PolarAxes):

        name = 'radar'
        PolarTransform = RadarTransform

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # rotate plot such that the first axis is at the top
            self.set_theta_zero_location('N')

        def fill(self, *args, closed=True, **kwargs):
            """Override fill so that line is closed by default"""
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.append(x, x[0])
                y = np.append(y, y[0])
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            # The Axes patch must be centered at (0.5, 0.5) and of radius 0.5
            # in axes coordinates.
            if frame == 'circle':
                return Circle((0.5, 0.5), 0.5)
            elif frame == 'polygon':
                return RegularPolygon((0.5, 0.5), num_vars,
                                      radius=.5, edgecolor="k")
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

        def _gen_axes_spines(self):
            if frame == 'circle':
                return super()._gen_axes_spines()
            elif frame == 'polygon':
                # spine_type must be 'left'/'right'/'top'/'bottom'/'circle'.
                spine = Spine(axes=self,
                              spine_type='circle',
                              path=Path.unit_regular_polygon(num_vars))
                # unit_regular_polygon gives a polygon of radius 1 centered at
                # (0, 0) but we want a polygon of radius 0.5 centered at (0.5,
                # 0.5) in axes coordinates.
                spine.set_transform(Affine2D().scale(.5).translate(.5, .5)
                                    + self.transAxes)
                return {'polar': spine}
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

    register_projection(RadarAxes)
    return theta

### Radar Charts

def makeHourRadarChart(timeStats:dict[int,int], msgAmount:int, language:str="SPANISH"):

    theta = radar_factory(24, frame='circle')

    data = [timeStats.get(i,0) / msgAmount for i in range(23,-1,-1)]
    spoke_labels = [f"{i} hrs" for i in range(23,-1,-1)]

    fig, ax = plt.subplots(figsize=(9, 9),
                            subplot_kw=dict(projection='radar'))
    
    ax.plot(theta, data, color="g")
    ax.fill(theta, data, facecolor="g", alpha=0.25, label='_nolegend_')
    ax.set_varlabels(spoke_labels)
    
    # plt.show()
    plt.tight_layout()
    plt.savefig("internal/global-hour-ranking.svg",transparent=False)
    plt.close()
    return

def makeHourRadarChartPerChatter(timeStats:dict[str, dict[int, int]], language:str="SPANISH"):

    theta = radar_factory(24, frame='circle')
    for chatter in timeStats.keys():
        if timeStats[chatter]:
            msgAmount = sum(timeStats[chatter].values())
            data = [(timeStats[chatter].get(i,0) / msgAmount) * 100 for i in range(23,-1,-1)]
            spoke_labels = [f"{i} hrs" for i in range(23,-1,-1)]

            fig, ax = plt.subplots(figsize=(9, 9),
                                    subplot_kw=dict(projection='radar'))

            ax.plot(theta, data, color="g")
            ax.fill(theta, data, facecolor="g", alpha=0.25, label='_nolegend_')
            ax.set_varlabels(spoke_labels)
            ax.set_title(chatter)

            plt.tight_layout()
            # plt.show()
            plt.savefig(f"internal/{chatter}-hour-ranking.svg",transparent=False)
            plt.close()
    return



if __name__ == "__main__":
    print("These won't work with plt.savefig(). Change them to plt.show() and uncomment the below functions for this to work.")
    # gc:Chat = parseChat(messages)   
    # mediaSentByChatter(gc)
    # makeMessagePie(gc)
    # makeTimeStackplot(gc)
    # global_minute_ranking, personal_minute_ranking, global_date_ranking, personal_date_ranking, global_hour_ranking, personal_hour_ranking = getTimeDicts(gc)
    # makeHourRadarChart(global_hour_ranking, gc.messageAmount)
    # makeHourRadarChartPerChatter(personal_hour_ranking)