% copy wav files from one place to another

origDir= 'S:\MarineCadastre\Monthly4500mTrackAboutCPA_KF';
targetDir = 'T:\Shared drives\MBARC_All\ShipNoise\MarineCadastre\Monthly4500mTrackAboutCPA';
folderList = dir(fullfile(origDir,'\*-*'));
nFolders = length(folderList);

for iFolder = 1:nFolders
    inDir = fullfile(folderList(iFolder).folder,folderList(iFolder).name);
    outDir = fullfile(targetDir,folderList(iFolder).name);
    if ~isdir(outDir)
        mkdir(outDir)
        
    end
    
    wavList = dir(fullfile(inDir,'*.wav'));
    for iW =1:length(wavList)
        source = fullfile(wavList(iW).folder,wavList(iW).name);
        destination = fullfile(outDir,wavList(iW).name);
        
        copyfile(source, destination)
    end
        
        
    
end


%%

origDir= 'S:\MarineCadastre\Monthly4500mTrackAboutCPA_KF';
targetDir = 'T:\Shared drives\MBARC_All\ShipNoise\MarineCadastre\Monthly4500mTrackAboutCPA';
folderList = dir(fullfile(origDir,'\*-*'));
nFolders = length(folderList);

for iFolder = 1:nFolders
    inDir = fullfile(folderList(iFolder).folder,folderList(iFolder).name);
    outDir = fullfile(targetDir,folderList(iFolder).name);
    if ~isdir(outDir)
        mkdir(outDir)
        
    end
    
    txtList = dir(fullfile(inDir,'*.txt'));
    for iW =1:length(txtList)
        source = fullfile(txtList(iW).folder,txtList(iW).name);
        destination = fullfile(outDir,txtList(iW).name);
        
        copyfile(source, destination)
    end
        
        
    
end