matList = dir('F:\MarineCadastre\Monthly4500mTrackAboutCPA_KF\**\*.mat');

for iM = 5:length(matList)
    myFile = fullfile(matList(iM).folder,matList(iM).name);
    load(myFile,'sdBRadon','sdB')
    try
        figure(10);
        subplot(1,2,1)
        imagesc(floor(sdB));set(gca,'ydir','normal','clim',[60,100])
        
        subplot(1,2,2)
        yMin = min(find(mean(sdBRadon,2)>10));
        yMax = max(find(mean(sdBRadon,2)>10));
        imagesc(sdBRadon)
        set(gca,'clim',[30,100])
        %ylim([yMin,yMax])
        1;
    catch
        fprintf('Radon failed on file %s\n',myFile)
        continue
    end
end