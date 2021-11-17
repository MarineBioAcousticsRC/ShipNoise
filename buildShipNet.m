options = trainingOptions('sgdm', ...
    'MiniBatchSize',4, ...
    'MaxEpochs',8, ...
    'Shuffle','every-epoch', ...
    'Verbose',true, ...
    'Plots','training-progress');

ds1 = fileDatastore('M:\ShipNoise_nnet_input\*.mat',...
    'ReadFcn',@loadPassage);
ds2 = fileDatastore('M:\ShipNoise_nnet_input\*.mat',...
    'ReadFcn',@loadCPA);
ds3 = fileDatastore('M:\ShipNoise_nnet_input\*.mat',...
    'ReadFcn',@loadCPA);
ds = combine(ds1,ds2,ds3);
read(ds)


imageInputSize= [11,11,1];
filterSize = 7;
numFilters = 1;
numClasses = 1;

%%
layers = [
    imageInputLayer(imageInputSize,'Normalization','none','Name','images')
    convolution2dLayer(filterSize,numFilters,'padding','same','Name','conv')
    reluLayer('Name','relu1')
    fullyConnectedLayer(1,'Name','fc1')
    concatenationLayer(1,2,'Name','concat')  
    reluLayer('Name','relu2')
    fullyConnectedLayer(numClasses,'Name','fc2')
    regressionLayer('Name','regression')]; %    

lgraph = layerGraph(layers);
layers2 = [featureInputLayer(numFeatures,'Name','features');
     fullyConnectedLayer(numClasses, 'Name','fc3')];

lgraph = addLayers(lgraph, layers2);
lgraph = connectLayers(lgraph, 'fc3', 'concat/in2');
% 
myNet = trainNetwork(ds,lgraph,options)