import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.ticker import MultipleLocator

class RSIndustryChart:
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None
        self.industries = None
        self.rs_recent = None
        self.rs_monthly = None
        self.x_cut = 50
        self.y_cut = 50
        self.colors = {
            'Strong': '#2B6CB0',
            'Improving': '#38A169',
            'Weakening': '#DD6B20',
            'Weak': '#C53030'
        }
        self.bg_alpha = 0.07
        self.fig = None
        self.ax = None
        
    def load_data(self):
        """Load data from Excel file"""
        self.df = pd.read_excel(self.filepath)
        self.industries = self.df['Industry'].values
        self.rs_recent = self.df['Percentile'].values
        self.rs_monthly = self.df['1 Month'].values
        
    def classify_quadrant(self, x, y):
        """Determine which quadrant a point belongs to"""
        if x >= self.x_cut and y >= self.y_cut:
            return 'Strong'
        elif x < self.x_cut and y >= self.y_cut:
            return 'Weakening'
        elif x < self.x_cut and y < self.y_cut:
            return 'Weak'
        else:
            return 'Improving'
    
    def setup_figure(self):
        """Initialize figure and axis"""
        self.fig, self.ax = plt.subplots(figsize=(14, 10))
        self.fig.patch.set_facecolor('white')
        self.ax.set_facecolor('white')
        self.ax.set_xlim(0, 102)
        self.ax.set_ylim(0, 100)
        
    def draw_quadrant_backgrounds(self):
        """Draw colored background rectangles for each quadrant"""
        quadrants = [
            ('Strong', 50, 50, 52, 52),
            ('Weakening', 0, 50, 50, 52),
            ('Weak', 0, 0, 50, 50),
            ('Improving', 50, 0, 52, 50)
        ]
        
        for name, x, y, width, height in quadrants:
            self.ax.add_patch(Rectangle(
                (x, y), width, height,
                color=self.colors[name],
                alpha=self.bg_alpha,
                zorder=0
            ))
    
    def plot_industries(self):
        """Plot scatter points and labels for each industry"""
        for i, industry in enumerate(self.industries):
            x = self.rs_recent[i]
            y = self.rs_monthly[i]
            quadrant = self.classify_quadrant(x, y)
            
            self.ax.scatter(
                x, y,
                s=30,
                color=self.colors[quadrant],
                alpha=0.9,
                zorder=3
            )
            
            self.ax.annotate(
                industry,
                xy=(x, y),
                xytext=(4, 0),
                textcoords='offset points',
                fontsize=7,
                ha='left',
                va='center',
                color='#2F2F2F',
                zorder=4,
                clip_on=True
            )
    
    def draw_cutoff_lines(self):
        """Draw vertical and horizontal cutoff lines"""
        self.ax.axvline(self.x_cut, linewidth=1.0, color='#9E9E9E', zorder=2)
        self.ax.axhline(self.y_cut, linewidth=1.0, color='#9E9E9E', zorder=2)
    
    def configure_grid(self):
        """Configure grid settings"""
        self.ax.xaxis.set_major_locator(MultipleLocator(10))
        self.ax.yaxis.set_major_locator(MultipleLocator(10))
        self.ax.grid(
            linestyle='--',
            linewidth=0.5,
            color='#D0D0D0',
            alpha=0.4,
            zorder=1
        )
    
    def add_quadrant_labels(self):
        """Add text labels for each quadrant"""
        labels = [
            ('STRONG', 75, 102, 'top'),
            ('WEAKENING', 25, 102, 'top'),
            ('WEAK', 25, -2, 'bottom'),
            ('IMPROVING', 75, -2, 'bottom')
        ]
        
        for text, x, y, va in labels:
            self.ax.text(
                x, y, text,
                fontsize=8,
                weight='semibold',
                ha='center',
                va=va,
                color='#4A4A4A'
            )
    
    def configure_axes(self):
        """Configure axis labels and styling"""
        self.ax.set_xlabel(
            'Recent Relative Strength (Percentile)',
            fontsize=12,
            color='#4A4A4A'
        )
        self.ax.set_ylabel(
            'Monthly Relative Strength (1-Month)',
            fontsize=12,
            color='#4A4A4A'
        )
        self.ax.tick_params(axis='both', labelsize=10, colors='#6E6E6E')
        
        for spine in ['top', 'right']:
            self.ax.spines[spine].set_visible(False)
        
        self.ax.spines['left'].set_color('#BDBDBD')
        self.ax.spines['bottom'].set_color('#BDBDBD')
    
    def add_title(self):
        """Add chart title"""
        self.ax.set_title(
            'Industry RS Recent vs Monthly',
            fontsize=10,
            weight='semibold',
            pad=20
        )
    
    def save_and_display(self, output_path='RS_Industry.png'):
        """Save figure and display"""
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def generate_chart(self):
        """Main method to generate the complete chart"""
        self.load_data()
        self.setup_figure()
        self.draw_quadrant_backgrounds()
        self.draw_cutoff_lines()
        self.configure_grid()
        self.plot_industries()
        self.add_quadrant_labels()
        self.configure_axes()
        self.add_title()
        self.save_and_display()


if __name__ == '__main__':
    chart = RSIndustryChart('RS_Industry.xlsx')
    chart.generate_chart()
