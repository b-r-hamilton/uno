path = 'C:\Users\bydd1\Downloads\file.xlsx';
data1 = xlsread(path);
x = data1(:, 3);
y = data1(:, 1);
modelfun = @(b,x)(b(1)*x.^b(2));
%modelfun = @(b,x)((x./b(1)).^(1/b(2)));
opts = statset('nlinfit');
opts.RobustWgtFun = 'bisquare';
beta0 = [25;0.5];
[beta, R, J, CovB, MSE] = nlinfit(x, y, modelfun, beta0, opts);
disp(beta)

xrange = min(x):.01:max(x);
[ypred,delta] = nlpredci(modelfun,xrange,beta,R,'Covar',CovB,...
                         'MSE',MSE,'SimOpt','on');
lower = ypred - delta;
upper = ypred + delta;

%%
figure()
plot(x,y,'ko') % observed data
hold on

plot(xrange,ypred,'k','LineWidth',2)
plot(xrange,[lower;upper],'r--','LineWidth',1.5)

xlabel('max discharge (cms)')
ylabel('meander wavelength (m)')
title('regression and 95% confidence interval')
legend('data','regression', '95% CI', 'Location', 'southeast')
ylim([1,max(y)])

%%
path = 'C:\Users\bydd1\Downloads\meandwave_for_brynn.csv';
data2 = readmatrix(path);
testx = data2(:, 2);
testy = (testx ./ beta(1)) .^ (1/beta(2));
figure()
plot(data2(:, 1), testy)
xlabel('time (years)')
ylabel('discharge')
title('reconstructed discharge values')
