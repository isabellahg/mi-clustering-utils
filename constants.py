
command = "java -jar your-artifactId-version-jar-with-dependencies.jar"


DBSCAN = 'MIDBSCAN'
EarthMoversDistance = 'EarthMoversDistance'
MahalanobisDistance = 'MahalanobisDistance'
HausdorffDistance = 'HausdorffDistance'

HausdorffTypes = range(4)


DISTANCE = "distance"
ACTUALNCLUSTERS = "actualNClusters"
CLUSTEREDBAGS = "clusteredBags"
UNCLUSTEREDBAGS = "unclusteredBags"
RMSSTD = "rmsstd"
SILHOUETTE = "silhouette"
XB = "xb"
DB = "db"
SDBW = "sdbw"
DBCV = "dbcv"
CONFUSIONMATRIX = "confusion matrix"
ENTROPY = "entropy"
PURITY = "purity"
RAND = "rand"
PRECISION = "precision"
RECALL = "recall"
F1 = "f1"
SPECIFICITY = "specificity"
TIME = "time"





DATASETKEY ='dataset'
STANDARDIZATIONKEY ='standardization'
DISTANCEFUNCTIONKEY ='distanceFunction'
DISTANCEFUNCTIONTYPEKEY ='distanceFunctionType'
CLUSTERINGKEY ='clustering'
MINPOINTSKEY ='minPoints'
EPSILONKEY ='epsilon'
DISTANCEANALYSIS = 'distanceAnalysis'


MAXIMIZE = 'maximize'
MINIMIZE = 'minimize'


DATASETS = [
                "musk1",
#                "musk2",
#                "BirdsBrownCreeper",
#                "BirdsChestnut-backedChickadee",
#                "BirdsHammondsFlycatcher",
#                "CorelAfrican",
#                "CorelAntique",
#                "CorelBattleships",
#                "Harddrive1",
                "ImageElephant",
#                "ImageFox",
#                "ImageTiger",
#                "Messidor",
                "mutagenesis3_atoms",
#                "mutagenesis3_bonds",
#                "mutagenesis3_chains",
                "Newsgroups1",
#                "Newsgroups2",
#                "Newsgroups3",
#                "suramin",
#                "DirectionEastwest",
#                "Thioredoxin",
#                "UCSBBreastCancer",
#                "Web1",
#                "Web2",
#                "Web3",
#                "Graz02bikes",
#                "Graz02car",
#                "Graz02people",
#                "standardMI_Maron",
#                "BiocreativeComponent",
#                "BiocreativeFunction",
#                "BiocreativeProcess",
]
JAR_NAME = 'mi-clustering-1.0-jar-with-dependencies.jar'
CLASS_NAME = 'miclustering.DbscanExperimentCli'