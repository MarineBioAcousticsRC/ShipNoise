function [h,sdB,specTime,specFreq] = plotShipPassWav_CINMS_B_180822(h,data,...
    shipTracks,s,cpa_m,t0,tn,d,tfDir,tfList,dataID)
plotOn = 0;
overlap = 50;
nfft = 10000;
noverlap = (overlap/100)*nfft;
fs = 10e3;
win = hanning(nfft);
% get TF
tfIdx = find(~cellfun(@isempty,strfind(tfList.textdata(:,1),dataID)));
tfNum = tfList.data(tfIdx-1);
[tfFolder, TFName] = pick_TF_subdirs(tfNum,tfDir);

%tfFolder = dir(fullfile(tfDir,[num2str(tfNum),'*']));
tfFile = fullfile(tfFolder,TFName.name); % dir(fullfile(tfFolder.folder,tfFolder.name,'*.tf'));

if isempty(tfFile)
    error('missing tf file')
end


% this seems to match the plot made by spectrogram with y-axis option
[~,specFreq,t,psd] = spectrogram(data,hanning(nfft),noverlap,nfft,fs,'psd');
[~, uppc] = fn_tfMap(tfFile,specFreq);
sdB = 10*log10(psd) + uppc;
specTime = t0+(t/(24*60*60));
if plotOn
    h = figure(132);
    % plot stuff
    date_fmt = 'mm/dd/yy HH:MM:SS';
    FS = 10;
    set(h,'Position',[ 75 75 1200 550 ] );
    subplot(1,2,1)
    sh = imagesc(specTime,specFreq,sdB);
    set(gca,'ydir','normal')
    % view(0,90);
    % axis tight;
    datetick('x','keepTicks','keepLimits')
    
    ax = gca;
    ap = get(ax,'Position');
    set(ax,'Position',[ap(1) ap(2) ap(3)*.9 ap(4)*.9]);
    
    % set(gca,'TickDir','out');
    colormap(jet(256));
    caxis([ 60 105 ]);
    cb = colorbar('FontSize',FS);
    sub1X = get(ax,'xlim');
    sub1Xtick = get(ax,'xtick');
    
    %cb = colorbar('Location','EastOutside','Position',[ .85 .1 0.025 0.75],'FontSize',FS);
    ylabel(cb,'dB re 1 \muPa^2/Hz');
    ylim([5,300])
    % build title string for plot
    titleStr = sprintf('%s',shipTracks(s).name{1});
    
    if ~isempty(shipTracks(s).IMO)
        titleStr = sprintf('%s IMO = %0.0f',titleStr,shipTracks(s).IMO(1));
    end
    
    titleStr = sprintf('%s\nMMSI = %d',titleStr,shipTracks(s).MMSI);
    titleStr = sprintf('%s\nMean SOG = %.2f [ kn ] CPA = %.2f [ m ]', ...
        titleStr, mean(shipTracks(s).SOG), cpa_m);
    if ~isempty(shipTracks(s).vData)
        titleStr = sprintf('%s draught = %.2f [m]', titleStr,mean(shipTracks(s).vData(:,3)));
    end
    titleStr = sprintf('%s\n%s - %s UTC',titleStr,datestr(t0,date_fmt),datestr(tn,date_fmt));
    
    t2 = title(titleStr);
    %tp = get(t2,'Position');
    % set(t2,'Position', [ tp(1) tp(2)+100 tp(3) ]);
    box on
    xlabel('Time [s]');
    ylabel('Frequency [Hz]');
    
    
    subplot(1,2,2)
    plot(shipTracks(s).dnums,d,'linewidth',2);
    xlabel('Time')
    ylabel('Horizontal Range (m)')
    set(gca,'xtick',sub1Xtick)
    datetick('x','keepTicks','keepLimits')
    xlim(sub1X)
    ax = gca;
    ap = get(ax,'Position');grid on;
    set(ax,'Position',[ap(1) ap(2) ap(3)*.9 ap(4)*.9]);
    ylim([0,6500])
    1;
end
end