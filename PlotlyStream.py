class PlotlyStream(object):
    
    def __init__(self, electricity_data, weather_data, stream_tokens):
        self.electricity = electricity_data
        self.weather = weather_data
        self.tokens = stream_tokens
    
    def create_plot(self, chart_title, x_title, y_title, y2_title, maxpoints):
        """Method to generate Plotly plot in notebook for rendering streaming data"""
        
        e_stream = Stream(token= self.tokens[0], maxpoints= maxpoints)
        trace1 = Scatter(x=[], y=[], mode='lines+markers', stream = e_stream, name='Usage')
        
        w_stream = Stream(token= self.tokens[1], maxpoints= maxpoints)
        trace2 = Scatter(x=[], y=[], mode='lines+markers', stream = w_stream, yaxis='y2', name='Temp')
        
        data = Data([trace1, trace2])
        
        # Initialize layout object
        layout = Layout(title= chart_title, 
                        showlegend=True,
                        xaxis= dict(title= x_title,
                                    range= [self.electricity.index.min(),self.electricity.index.max()],
                                    ticks='outside',
                                    type='date'
                                  ),
                        yaxis= dict(title = y_title,
                                    range=[self.electricity.min(),self.electricity.index.max()],
                                  ),
                        yaxis2 = dict(title = y2_title,
                                      range=[self.weather.min(), self.weather.max()],
                                      overlaying='y',
                                      side='right'
                                     ),
                        hovermode='closest'
                       )
        
        # Create figure object
        fig = Figure(data=data, layout=layout)
        
        # (@) Send fig to Plotly, initialize streaming plot, open new tab
        return py.iplot(fig, filename='Pecan Street Streaming Electricity Usage')
    
    def plot_stream(self, plot_freq=0.2, start_delay=0.1):
        """Method to write data to Plotly servers to render on graph"""
        
        s1 = py.Stream(self.tokens[0])
        s2 = py.Stream(self.tokens[1])
        
        s1.open()
        s2.open()
        
        counter = 0
        N = 500
        
        # Create small delay before plotting begins
#         time.sleep(start_delay)
        
        electricity = self.electricity.iterrows()
        weather = self.weather.iterrows()
        
        while counter < N:
            counter += 1
            
            timestamp1, usage = electricity.next()
            timestamp2, temperature = weather.next()
            
            # .strftime('%Y-%m-%d %H.%f')
            
            times = []
            usages = []
            temperatures = []
            
            x1 = timestamp1.strftime('%Y-%m-%d %H:%M:%S.%f')
            y1 = usage
            
            x2 = timestamp2.strftime('%Y-%m-%d %H:%M:%S.%f')
            y2 = temperature
            
            s1.write(dict(x=x1, y=y1))
            s2.write(dict(x=x2, y=y2))
            time.sleep(plot_freq)
        
        s1.close()
        s2.close()