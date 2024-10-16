let myChart = null;
let myDoughnutChart = null;
let myLeadChart = null;
let myFollowupChart = null;
let myPerformanceChart = null;
let myAcieventmentChart = null;
let myteamWiseChart = null;
const showLoader = () => {
  document.getElementById('loader').style.display = 'block';
}

const hideLoader = () => {
  document.getElementById('loader').style.display = 'none';
}

const PerformanceAPI = async (option) =>{
  showLoader(); 
  let url = `http://182.70.253.15:8000/admin/Performance-Graph`;
  if (option){
     url += `?startDate=${option.startDate}&endDate=${option.endDate}&teamId=${option.teamId}&memberName=${option.memberName}` 
  }
  try{
    const response = await fetch(url);
    const data = await response.json();

    EmpPerformance(data); 
    EmpAchievement(data); 
    TeanAPI();
    
  }catch(error){

    console.error(error)
  }finally{
    hideLoader();
  }
}

const APiCall = async (option) => {
  showLoader(); 
  let apiUrl = `http://182.70.253.15:8000/admin/Graph-Values`;
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
  const dataSet = [
            {
                label: 'Hot',
                data: [GetData.hot_leads],
                backgroundColor: 'rgb(255, 99, 132)',
            },
            {
                label: 'Opportunity',
                data: [GetData.opportunity_leads],
                backgroundColor: 'rgb(255, 205, 86)',
            },
            {
                label: 'Proposal',
                data: [GetData.proposal_leads],
                backgroundColor: 'rgb(75, 192, 192)',
            },
            {
                label: 'Cold',
                data: [GetData.cold_leads],
                backgroundColor: 'rgb(54, 162, 235)',
            }
  ];
  var ctx = document.getElementById('myChart').getContext('2d');
  if (myChart) {
    myChart.destroy();
  }
  myChart = new Chart(ctx, {
      type: 'bar',
      data: {
          labels: ['Lead Types'], 
          datasets: dataSet
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
              legend: {
                display: true,  // Show the legend (one entry per bar)
                position: 'top', // Position legend at the top of the chart
                
              },
              datalabels: {
                  anchor: 'end',
                  align: 'start',  // Adjust alignment to avoid overlapping
                  color: '#2A2A50',
                  font: {
                      weight: 'bold',
                      size: 14  // Adjust the font size for the data labels
                  },
                  padding: {
                      top: 6,  // Add padding above the labels
                      bottom: 6  // Add padding below the labels
                  },
                  formatter: function(value) {
                      return value;  // Show the data value on each bar
                  }
              }
          },
         
      },
      plugins: [ChartDataLabels]  // Ensure ChartDataLabels plugin is included to show data values
  });
}





const LeadStage = (GetData) => {
  const data = {
      labels: ['Open', 'Close'],
      datasets: [{
          label: 'Lead Stages',
          data: [GetData.total_open_leads, GetData.total_close_leads],
          backgroundColor: [
              'rgb(54, 162, 235)',  // blue
              'rgb(255, 205, 86)',  // yellow
          ]
      }]
  };

  const config = {
      type: 'doughnut',
      data: data,
      options: {
          responsive: true,
          plugins: {
              legend: {
                  position: 'top',
              },
              title: {
                  display: true,
                  text: 'Lead Stages Distribution'
              },
              datalabels: {
                  formatter: (value, ctx) => {
                      const label = ctx.chart.data.labels[ctx.dataIndex];
                      // return `${label}: ${value}`; // Display label and value
                      return `${value}`; // Display value
                  },
                  color: 'black', // Text color
                  font: {
                      size: 12,
                  }
              }
          }
      },
      plugins: [ChartDataLabels]  // Include ChartDataLabels plugin
  };

  var ctx = document.getElementById('myDoughnutChart').getContext('2d');
  if (myDoughnutChart) {
    myDoughnutChart.destroy();
  }
  myDoughnutChart = new Chart(ctx, config);
}



const Visit = (GetData) => {
  const dataSet = [
    {
      label: 'Home',  // Dataset for Home visits
      data: [GetData.total_home],  // Data for Home visits
      backgroundColor: 'rgb(75, 192, 192)', 
    },
    {
      label: 'Corporate',  // Dataset for Corporate visits
      data: [GetData.total_corporate],  // Data for Corporate visits
      backgroundColor: 'rgb(54, 162, 235)',
    },
    {
      label: 'Sage Mitra',  // Dataset for Sage Mitra visits
      data: [GetData.total_sagemitra],  // Data for Sage Mitra visits
      backgroundColor: 'rgb(86, 59, 191)',
    },
    {
      label: 'Site Visit',  // Dataset for Site visits
      data: [GetData.total_site],  // Data for Site visits
      backgroundColor: 'rgb(255, 205, 86)',
    }
  ];

  var ctx = document.getElementById('myLeadChart').getContext('2d');

  if (myLeadChart) {
    myLeadChart.destroy();  // Destroy the previous chart if it exists
  }

  myLeadChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Visit Types'],  // X-axis label for the categories
      datasets: dataSet  // Use the defined datasets
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
        legend: {
          display: true,  // Show the legend
          position: 'top',  // Position the legend at the top
        },
        datalabels: {
          anchor: 'end',
          align: 'start',  // Adjust alignment to avoid overlapping
          color: '#2A2A50',
          font: {
            weight: 'bold',
            size: 14  // Adjust the font size for the data labels
          },
          padding: {
            top: 6,  // Add padding above the labels
            bottom: 6  // Add padding below the labels
          },
          formatter: function(value) {
            return value;  // Show the data value on each bar
          }
        }
      },
      layout: {
        padding: {
          top: 10,
          right: 10,
          bottom: 20,  // Adjust bottom padding for the layout
          left: 10
        }
      }
    },
    plugins: [ChartDataLabels]  // Ensure ChartDataLabels plugin is included
  });
}



const LeadStates = (GetData) => {
  var ctx = document.getElementById('myFollowupChart').getContext('2d');
  
  if (myFollowupChart) {
    myFollowupChart.destroy();  // Destroy the existing chart instance if it exists
  }

  // Define datasets for each category
  const dataSet = [
    {
      label: 'Total Leads',
      data: [GetData.total_Leads],  // Data for Total Leads
      backgroundColor: 'rgb(54, 162, 235)',  // Color for Total Leads bar
    },
    {
      label: 'Follow Up',
      data: [GetData.total_followUp],  // Data for Follow Up
      backgroundColor: 'rgb(153, 102, 255)',  // Color for Follow Up bar
    },
    {
      label: 'New Leads',
      data: [GetData.total_new_leads],  // Data for New Leads
      backgroundColor: 'rgb(201, 203, 207)',  // Color for New Leads bar
    }
  ];

  myFollowupChart = new Chart(ctx, {
    type: 'bar',  // Specify the chart type
    data: {
      labels: ['Leads States'],  // X-axis label, common for all datasets
      datasets: dataSet  // Use the defined datasets
    },
    options: {
      responsive: true,
      scales: {
        x: {
          ticks: {
            font: {
              size: 16  // Font size for X-axis ticks
            }
          }
        },
        y: {
          beginAtZero: true  // Y-axis starts at zero
        }
      },
      plugins: {
        legend: {
          display: true,  // Show the legend
          position: 'top',  // Position the legend at the top
        },
        datalabels: {
          anchor: 'end',  // Anchor the labels to the end of the bar
          align: 'start',   // Align the labels at the end of the bar
          color: '#2A2A50',
          font: {
            weight: 'bold',
            size: 14  // Font size for data labels
          },
          padding: {
            top: 6,  // Padding above the labels
            bottom: 6  // Padding below the labels
          },
          formatter: function(value) {
            return value;  // Show the data value on each bar
          }
        }
      },
      layout: {
        padding: {
          top: 10,
          right: 10,
          bottom: 20,  // Adjust bottom padding for the layout
          left: 10
        }
      }
    },
    plugins: [ChartDataLabels]  // Include the ChartDataLabels plugin
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
        label: 'Average Performance',
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
            weight: 'bold',
            size: 12 // Adjust size as needed
          },
          formatter: function(value) {
            return value ; // Display percentage for each bar
          },
        },
        legend: {
          display: false,  // hide the legend          
        }
      },
      layout: {
        padding: {
          top: 30,  // Add top padding
        }
      }
    },
    plugins: [ChartDataLabels] // Ensure the ChartDataLabels plugin is included
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
        },
        legend: {
          display: false,  // hide the legend          
        }
      },
      layout: {
        padding: {
          top: 30,  // Add top padding
          
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

const TeanAPI = async () => {
  console.log("")
    const url = "http://10.22.130.15:8000/admin/Team-API"

    try{
      const response = await fetch(url);
      const data = await response.json();
      console.log("==", data)
      TeamWiseData(data);
    }
    catch (error){
      console.error(error.message)
    }
    finally{
      
    }
}

const TeamWiseData = (GetData) => {
  // Extract team data from GetData.data
  const teamData = Object.values(GetData.data);

  // Initialize arrays to hold employee names and lead counts
  let employeeNames = [];
  let hotLeads = [];
  let opportunityLeads = [];
  let proposalLeads = [];
  let coldLeads = [];

  // Loop through each team and gather data for employees
  teamData.forEach(team => {
    team.employees.forEach(employee => {
      employeeNames.push(employee.Employee_name);  // Add employee names
      hotLeads.push(employee.hot_leads);  // Add hot leads count
      opportunityLeads.push(employee.opportunity_leads);  // Add opportunity leads count
      proposalLeads.push(employee.proposal_leads);  // Add proposal leads count
      coldLeads.push(employee.cold_leads);  // Add cold leads count
    });
  });

  // Define the datasets for Chart.js
  const dataSet = [
    {
      label: 'Hot Leads',
      data: hotLeads,  // Data for hot leads
      backgroundColor: 'rgba(255, 99, 132, 0.6)',  // Red color
    },
    {
      label: 'Opportunity Leads',
      data: opportunityLeads,  // Data for opportunity leads
      backgroundColor: 'rgba(54, 162, 235, 0.6)',  // Blue color
    },
    {
      label: 'Proposal Leads',
      data: proposalLeads,  // Data for proposal leads
      backgroundColor: 'rgba(75, 192, 192, 0.6)',  // Green color
    },
    {
      label: 'Cold Leads',
      data: coldLeads,  // Data for cold leads
      backgroundColor: 'rgba(153, 102, 255, 0.6)',  // Purple color
    }
  ];

  // Get the context for the chart
  var ctx = document.getElementById('TeamWise').getContext('2d');

  // Destroy the previous chart if it exists
  if (myteamWiseChart) {
    myteamWiseChart.destroy();
  }

  // Create the new chart
  myteamWiseChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: employeeNames,  // X-axis labels (employee names)
      datasets: dataSet  // Use the defined datasets for different lead types
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
        legend: {
          display: true,  // Show the legend
          position: 'top',  // Position the legend at the top
        },
        datalabels: {
          anchor: 'end',
          align: 'start',  // Adjust alignment to avoid overlapping
          color: '#2A2A50',
          font: {
            weight: 'bold',
            size: 14  // Adjust the font size for the data labels
          },
          padding: {
            top: 6,
            bottom: 6
          },
          formatter: function(value) {
            return value;  // Show the data value on each bar
          }
        }
      },
      layout: {
        padding: {
          top: 10,
          right: 10,
          bottom: 20,
          left: 10
        }
      }
    },
    plugins: [ChartDataLabels]  // Ensure ChartDataLabels plugin is included
  });
};
