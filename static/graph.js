let myChart = null;
let myDoughnutChart = null;
let myLeadChart = null;
let myFollowupChart = null;
let myPerformanceChart = null;
let myAcieventmentChart = null;

const showLoader = () => {
  document.getElementById('loadertext').style.display = 'block';
}

const hideLoader = () => {
  document.getElementById('loadertext').style.display = 'none';
}

const PerformanceAPI = async (option) =>{
  showLoader(); 
  let url = `http://10.22.130.15:8000/admin/Performance-Graph`;
  if (option){
     url += `?startDate=${option.startDate}&endDate=${option.endDate}&teamId=${option.teamId}&memberName=${option.memberName}` 
  }
  try{
    const response = await fetch(url);
    const data = await response.json();

    EmpPerformance(data); 
    EmpAchievement(data); 
    
  }catch(error){

    console.error(error)
  }finally{
    hideLoader();
  }
}

const APiCall = async (option) => {
  showLoader(); 
  let apiUrl = `http://10.22.130.15:8000/admin/Graph-Values`;
  if (option){
    apiUrl += `?startDate=${option.startDate}&endDate=${option.endDate}&teamId=${option.teamId}&memberName=${option.memberName}` 
  }
  
  
  try{
    const response = await fetch(apiUrl);
    const data = await response.json();   

    LeadType(data);
    LeadStage(data);
    Visit(data);
    LeadStates(data);
    TabCards(data);
    PerformanceAPI(option);
    Dropdown(data.membersList);
   
    return data;
  }
  catch(error){
    console.error(error)
  }finally{
    hideLoader();
  }
  
} 

const LeadType = (GetData) => {
  var ctx = document.getElementById('myChart').getContext('2d');
  if (myChart) {
    myChart.destroy();
  }
  myChart = new Chart(ctx, {
      type: 'bar',
      data: {
          labels: ['Hot', 'Opportunity', 'Proposal', 'Cold'],
          datasets: [{
              label: 'Lead Type wise leads',
              data: [GetData.hot_leads, GetData.opportunity_leads, GetData.proposal_leads, GetData.cold_leads],
              backgroundColor: [
                  'rgb(255, 99, 132)', 
                  'rgb(255, 205, 86)',
                  'rgb(75, 192, 192)', 
                  'rgb(54, 162, 235)',
              ],
              // borderColor: [
              //     'rgba(75, 192, 192, 1)',
              //     'rgba(54, 162, 235, 1)',
              //     'rgba(255, 206, 86, 1)',
              //     'rgba(255, 99, 132, 1)',
              // ],
              // borderWidth: 2
          }]
      },
      options: {
        responsive: true,
          scales: {
                x: {
                  ticks: {
                      font: {
                          size: 16
                      }
                  }
              },
              y: {
                  beginAtZero: true
              }
          },
          plugins: {
              datalabels: {
                  anchor: 'end',
                  align: 'end',
                  color: '#2A2A50',
                  font: {
                      weight: 'bold'
                  },
                  formatter: function(value, context) {
                      return value; 
                  }
              }
          }
      },
      plugins: [ChartDataLabels] 
  });
}





const LeadStage = (GetData) => {
  const data = {
      labels: ['Open', 'Close'],
      datasets: [{
          label: 'Lead Stages',
          data: [GetData.total_open_leads, GetData.total_close_leads],
          backgroundColor: [
            // 'rgb(255, 99, 132)',      //red
            // 'rgb(75, 192, 192)',      //green
                'rgb(54, 162, 235)',     //blue
                'rgb(255, 205, 86)',     //yellow
              // 'rgba(153, 102, 255)',  // purple
              // 'rgba(201, 203, 207)'   // black
                
          ],
          // borderColor: [
          //   'rgba(54, 162, 235, 1)',
          //   'rgba(255, 99, 132, 1)',
            
          // ],
          // borderWidth: 2
      }]
  };

  const config = {
      type: 'doughnut',
      data: data,
      options: {
          x: {
            ticks: {
                font: {
                    size: 16 // Adjust the font size for x-axis labels
                }
            }
        },
          responsive: true,
          plugins: {
              legend: {
                  position: 'top',
              },
              title: {
                  display: true,
                  text: 'Lead Stages Distribution'
              }
          }
      },
  };

  var ctx = document.getElementById('myDoughnutChart').getContext('2d');
  if (myDoughnutChart) {
    myDoughnutChart.destroy();
  }
  myDoughnutChart = new Chart(ctx, config);
}



const Visit = (GetData) => {
  var ctx = document.getElementById('myLeadChart').getContext('2d');
  if (myLeadChart) {
    myLeadChart.destroy();
  }
  myLeadChart = new Chart(ctx, {
      type: 'bar',
      data: {
          labels: ['Home', 'Corporate', 'Sage Mitra', 'Site Visit'],
          datasets: [{
              label: 'Acc Tracker',
              data: [GetData.total_home, GetData.total_corporate, GetData.total_sagemitra, GetData.total_site],
              backgroundColor: [

                'rgb(75, 192, 192)', 
                'rgb(54, 162, 235)',
                'rgb(86, 59, 191)',
                'rgb(255, 205, 86)',
                
              ],
              // borderColor: [
              //   'rgba(255, 206, 86, 1)',
              //   'rgba(54, 162, 235, 1)',
              //   'rgba(255, 99, 132, 1)',
              //   'rgba(75, 192, 192, 1)',
              // ],
              // borderWidth: 2
          }]
      },
      options: {
        responsive: true,
          scales: {
            x: {
              ticks: {
                  font: {
                      size: 16
                  }
              }
          },
              y: {
                  beginAtZero: true
              }
          },
          plugins: {
              datalabels: {
                  anchor: 'end',
                  align: 'end',
                  color: '#2A2A50',
                  font: {
                      weight: 'bold'
                  },
                  formatter: function(value, context) {
                      return value; 
                  }
              }
          }
      },
      plugins: [ChartDataLabels] 
  });
}



const LeadStates = (GetData) => {
  var ctx = document.getElementById('myFollowupChart').getContext('2d');
  if (myFollowupChart) {
    myFollowupChart.destroy();
  }
  myFollowupChart = new Chart(ctx, {
      type: 'bar',
      data: {
          labels: ['Total Leads', 'Follow Up', 'New Leads'],
          datasets: [{
              data: [GetData.total_Leads, GetData.total_followUp, GetData.total_new_leads],
              backgroundColor: [
                'rgb(54, 162, 235)',
                'rgb(153, 102, 255)', // purple
                'rgb(201, 203, 207)' // black
                
              ],
              // borderColor: [
              //   'rgba(54, 162, 235, 1)',
              //     'rgba(75, 192, 192, 1)',
              //     'rgba(255, 99, 132, 1)',
                 
              // ],
              // borderWidth: 2
          }]
      },
      options: {
        responsive: true,
          scales: {
            x: {
              ticks: {
                  font: {
                      size: 16 
                  }
              }
          },
              y: {
                  beginAtZero: true
              }
          },
          plugins: {
              datalabels: {
                  anchor: 'end',
                  align: 'end',
                  color: '#2A2A50',
                  font: {
                      weight: 'bold'
                  },
                  formatter: function(value, context) {
                      return value; 
                  }
              }
          }
      },
      plugins: [ChartDataLabels] 
  });
}

const generateColors = (index, length) => {
  const startColor = [75, 192, 192]; // Green
  const endColor = [255, 99, 132]; // Red

  const ratio = index / (length - 1);

  const color = startColor.map((start, i) => 
    Math.round(start + ratio * (endColor[i] - start))
  );

  return `rgba(${color[0]}, ${color[1]}, ${color[2]})`;
};

const EmpPerformance = (GetData) => {
  const targetArray = Object.values(GetData.targets);

  // Sort in descending order by average percentage
  targetArray.sort((b, a) => a.average_percentage - b.average_percentage);

  const labels = targetArray.map(item => item.member_name);
  const data = targetArray.map(item => item.average_percentage);

  const backgroundColors = targetArray.map((item, index) => 
    item.average_percentage > 0 ? generateColors(index, targetArray.filter(item => item.average_percentage > 0).length) : 'rgb(75, 192, 192)' 
  );

  var ctx = document.getElementById('myPerformanceChart').getContext('2d');

  if (myPerformanceChart) {
    myPerformanceChart.destroy();
  }

  myPerformanceChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Average Performance (%)',
        data: data, 
        backgroundColor: backgroundColors,
        borderColor: backgroundColors.map(color => color.replace('0.6', '1')), 
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      scales: {
        x: {
          ticks: {
              font: {
                  size: 14 // Adjust the font size for x-axis labels
              }
          }
      },
        y: {
          beginAtZero: true
        }
      },
      plugins: {
        datalabels: {
          anchor: 'end',
          align: 'end',
          color: '#2A2A50',
          font: {
            weight: 'bold'
          },
          formatter: function(value) {
            return value;
          }
        }
      }
    },
    plugins: [ChartDataLabels]
  });
};

const EmpAchievement = (GetData) => {
  const targetArray = Object.values(GetData.data);
  
  // Sort in descending order by average percentage
  targetArray.sort((b, a) => a.average_percentage - b.average_percentage);

  const labels = targetArray.map(item => item.member_name);
  const data = targetArray.map(item => item.average_percentage);

  const backgroundColors = targetArray.map((item, index) => 
    item.average_percentage > 0 ? generateColors(index, targetArray.filter(item => item.average_percentage > 0).length) : 'rgb(75, 192, 192)' 
  );

  var ctx = document.getElementById('myAchivementsChart').getContext('2d');

  if (myAcieventmentChart) {
    myAcieventmentChart.destroy();
  }

  myAcieventmentChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Average Achievements (%)',
        data: data, 
        backgroundColor: backgroundColors,
        borderColor: backgroundColors.map(color => color.replace('0.6', '1')), 
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      scales: {
        x: {
          ticks: {
              font: {
                  size: 14 
              }
          }
      },
        y: {
          beginAtZero: true
        }
      },
      plugins: {
        datalabels: {
          anchor: 'end',
          align: 'end',
          color: '#2A2A50',
          font: {
            weight: 'bold'
          },
          formatter: function(value) {
            return value;
          }
        }
      }
    },
    plugins: [ChartDataLabels]
  });
};






document.addEventListener("DOMContentLoaded", async function() {  

  const GetData = await APiCall(); 
});

let changed = false;
var option = {
  startDate:"",
  endDate:"",
  teamId:"",
  memberName:"",
}


const handleDateChange = () => {
  
  const startDate = document.getElementById('StartDate').value; 
  const endDate = document.getElementById('EndDate').value; 
  const team = document.getElementById('teamSelect').value;
  const member = document.getElementById('memberSelect').value;

  if ((startDate.length !== 0) && (endDate.length !== 0) ) {
    changed = true;
    option.startDate = startDate;
    option.endDate = endDate;
  }
  if (team.length > 0){    
    option.teamId = team;
    changed= true;
  }
  if (member.length > 0){    
    option.memberName = member;
    changed= true;
  }
  if (changed){
    APiCall(option);
  }
  option = {
    startDate:"",
    endDate:"",
    teamId:"",
    memberName:"",
  }
}



const Dropdown = (membersList) =>{
  const select = document.getElementById('memberSelect');

  if (membersList.length == 1) return ; 
  select.innerHTML = `<option selected value=''>Select Member</option>` + membersList.map(member => (`<option  value='${member.member_name}'>${member.member_name}</option>`))
}




const TabCards = (GetData) => {

  const tabArr = ['newleads', 'totalleads', 'sitevisit', 'homevisit', 'corporatevisit'];


  const dataMap = {
    newleads: GetData.total_new_leads,                  
    totalleads: GetData.total_open_leads,              
    sitevisit: GetData.total_site,             
    homevisit: GetData.total_home,
    corporatevisit: GetData.total_corporate
  };

  tabArr.map((tabs) => {
    const tabAttr = document.getElementById(tabs);
    
    if (tabAttr && dataMap[tabs] !== undefined) {

      
      tabAttr.setAttribute('data-target', dataMap[tabs]);
      tabAttr.innerText = dataMap[tabs];   
    }
  });
  
  console.log('Data-targets set successfully');
};