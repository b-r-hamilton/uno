path = 'D:\Data\river data\VicksburgHistoricStage.xlsx';
x = readtable(path);

%%
time = x{:, 1};
stage = x{:, 2};

%%
figure()
plot(time, stage)
xlabel('time')
ylabel('stage (ft)')
title('Stage at Vicksburg')
