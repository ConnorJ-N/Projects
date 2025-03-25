import pandas as pd
try:
    import pacmap
    import umap
except ImportError:
    print("PaCMAP and/ or UMAP cannot be imported")
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler
    
class Dimensionality_Reduction():
    
    def __init__(self, data, minmax=True):
        self.data = data
        self.features = self.data.columns
        self.minmax = minmax
        
        if self.minmax is True:
            scaler = MinMaxScaler()
            self.data = pd.DataFrame(scaler.fit_transform(self.data), columns=self.features)
        
        
    def pacmap_representation(self, neighbours=None, n_components=2, init="pca"):
        embedding = pacmap.PaCMAP(n_components=n_components, n_neighbours=neighbours, distance="angular")
        x_transformed = embedding.fit_transform(self.data, init=init)
        return x_transformed
    
    def umap_representation(self, neighbours=None, n_components=2, init="spectral"):
        embedding = umap.UMAP(n_neighbours=neighbours, n_components=n_components, init=init).fit_transform(self.data)
        return embedding
    
    def tsne_representation(self, perplexity=12, exaggeration=4, n_components=2, init="random"):
        tsne_x = TSNE(n_components=n_components, perplexity=perplexity, early_exaggeration=exaggeration, init=init)
        embedding = tsne_x.fit_transform(self.data)
        return embedding
    
    def pca_representation(self, components=2):
        embedding = PCA(n_components=components)
        embedding = embedding.fit_transform(self.data)
        return embedding
        
        
        
        