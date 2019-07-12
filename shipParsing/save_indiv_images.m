clearvars

inFileList = dir('J:\ShippingCINMS_data\2*.mat');
outDir = 'J:\ShippingCINMS_data\indiv_files';

for iFile = 2:size(inFileList,1)
    load(fullfile(inFileList(iFile).folder,inFileList(iFile).name))
    imageStackScaled = (imageStack + 200)./(200);
%     for iPass = 1:size(imageStack,3)
%         %thisImage = imageStack(:,:,iPass);
%         
%         
%         thisImage_scaled = imageStackScaled(:,:,iPass);
%         thisIMO = IMO(iPass);
%         thisDateTime = transitDateTime{iPass};
%         thisMeanSOG = meanSOG(iPass);
%         thisCPADist =  CPADist(iPass);
%         thisShipSize = shipSize(iPass);
%         thisShipType = shipType{iPass};
%         thisDraught = draught(iPass);
%         f2 = 0:5000/1875:5000;
%         log10sx = log10(1600);
%         log10sxVec = (0:(log10sx/1024):log10sx);
%         log10xq = 10.^(log10sxVec(2:end));
%         fLog10 = interp1(f2,log10xq);
%         imageSaveName = ['IMO',num2str(thisIMO), '_',datestr(thisDateTime, 'yyyymmddHHMMSS')];
%         save(fullfile(outDir,[imageSaveName,'.mat']),'thisImage_scaled','thisShipType','thisIMO',...
%             'thisDateTime','thisMeanSOG','thisCPADist','thisShipSize','thisDraught','-v7.3');
%         h1 = imagesc(thisImage_scaled);
%         h2 = gca;
%         h2.YTick = [1,217,507,823];
%         set(h2,'YTickLabel', {'0','10','100','1000'});
%         ylabel('Freqency (kHz)')
%         xlabel('Normalized Duration')
%         colormap(jet)
%         set(gca,'ydir','normal')
%         colorbar
%         
%         caxis([0 .8])
%         
%         print(fullfile(outDir,[imageSaveName,'.jpg']),'-djpeg');
%         
%         
%    end
    thisDateTime = transitDateTime{1};

    h1 = imagesc(mean(imageStackScaled,3));
    h2 = gca;
    h2.YTick = [1,217,507,823];
    set(h2,'YTickLabel', {'0','10','100','1000'});
    ylabel('Freqency (kHz)')
    xlabel('Normalized Duration')
    colormap(jet)
    set(gca,'ydir','normal')
    colorbar
    caxis([.3 .7])
    
    title(sprintf('Normalized mean noise %s',datestr(thisDateTime,'mmm-yy')))
    imageMeanSaveName = fullfile(outDir,['mean_noise_',datestr(thisDateTime,'yyyymm')]);
    
    print([imageMeanSaveName,'.jpg'],'-djpeg');
    saveas(gca,[imageMeanSaveName,'.fig']);
    
end
