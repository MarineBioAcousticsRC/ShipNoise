matList = dir('M:\MarineCadastre\Monthly4500mTrackAboutCPA_KF\**\*.mat');

for iM = 1:length(matList)
    myFile = fullfile(matList(iM).folder,matList(iM).name);
    load(myFile)
    try
        [sdBRadon,projectionAngles,xResize,yResize] = calc_radon(thisShipTrack,distSpec(:,1:300)',uRange1,f_rng(1:300));

    catch
        fprintf('Radon failed on file %s\n',myFile)
        continue
    end
    
%     try
%         [sdBRadon,projectionAngles] = calc_radon(thisShipTrack,sdB,specTime);
%     catch
%         fprintf('Radon failed on file %s\n',myFile)
%         continue
%     end

    save(myFile,'sdBRadon','projectionAngles',...
            'xResize','yResize','-append')
    projectionAngles = [];
    sdBRadon = [];
end