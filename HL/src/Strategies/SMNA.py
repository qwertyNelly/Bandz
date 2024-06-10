
import threading

class smma():

    def __init__(self, series : list[], n : int ) -> None:    
        out : list[] = []
        for i in range(1,len(series)):
            temp=out[-1]*(n-1)+series[i]
            out.append(temp/n)
        
        self.sma = out

    @classmethod
    def run(cls):
        smnath : threading.Thread = threading.Thread(smma, 'SMNA')
        try:
            smnath.start()
        except RuntimeError as e:
            raise e
        


    