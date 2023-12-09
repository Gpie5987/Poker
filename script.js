document.addEventListener("DOMContentLoaded", function() {
    // 获取图表容器
    const chart = document.getElementById("chart");
    
    // 取得python計算結果
    var ip_rst = get_ip_rst();
    var oop_rst = get_oop_rst();
    var board_txt_list = get_board();
    
    // 將結果顯示在圖表上
    showBoard(board_txt_list);
    printPoint(ip_rst,'ip_point');
    printPoint(oop_rst,'oop_point');
    
    function printPoint(rst,point_class){
      let time = 0;
    // 遍历数据点并在图表中创建点
      for(let i = 0; i < rst.length; i++){
      if (rst[i] == null){continue;}
      const pointElement = document.createElement("div");
      pointElement.className = point_class;
      //pointElement.style.top = 0 + "px";
      pointElement.style.left = 15*i + "px";
      let amt = rst[i].length;
      let pr = 99 - time;
      time++;
      pointElement.addEventListener("mouseenter", (event) => {removeElement();showPR(pr,amt);showPic(event,rst[i]);});
      chart.appendChild(pointElement);
      }
    }

    //建立儀表板內容
    function showBoard(board_txt_list){
      //顯示board
      const dash_board_div = document.createElement('div');
      dash_board_div.className = 'dash_board_div';
      board_txt_list.forEach(card => {
        image = document.createElement('img');
        image.className = 'card';
        image.src = 'cards_pic/'+ card[0] + card[1] + '.PNG';
        dash_board_div.appendChild(image);
      })
      chart.appendChild(dash_board_div);
      //顯示IP與OOP牌力分佈
      ip_distribution = get_ip_distribution();
      oop_distribution = get_oop_distribution();
      ip_distribution_div =create_distribution_div(ip_distribution,'IP');
      oop_distribution_div =create_distribution_div(oop_distribution,'OOP');
      dash_board_div.appendChild(ip_distribution_div);
      dash_board_div.appendChild(oop_distribution_div);
    }
    
    //建立牌力分佈div標籤
    function create_distribution_div(distribution,position){
      const distribution_div = document.createElement('pre');
      distribution_div.style.fontSize = 17 + "px";
      let sum = calculate_dict_sum(distribution);
      distribution_div.innerHTML =  position + '<br>';
      for (let type in distribution) {
        percentage = distribution[type] / sum * 100;
        percentage = percentage.toFixed(1);
        console.log('type length:' + type.length);
        distribution_div.innerHTML += type + ':'.padEnd(20 - type.length) + distribution[type] + '(' + percentage +'%)' + '<br>';
      };
      return distribution_div;
    }

    //將字典的值加總
    function calculate_dict_sum(card_distribution){
      let sum = 0;
      for (let type in card_distribution) {
        sum += card_distribution[type];
      }
      return sum;
    }

    //當鼠標懸浮到點上時顯示手牌
    function showPic(event,rst){
      const hands_container = document.createElement('div');
      hands_container.addEventListener('click',() => removeElement())
      hands_container.className = 'hands_container';
      hands_container.style.left = 15 + event.pageX + "px";
      hands_container.style.top = 15 + event.pageY + "px";
      console.log('x:'+event.offsetX+'y:'+event.offsetY);
      rst.forEach(hand => {
        const hand_div = document.createElement('div');
        hand_div.className = 'hand';
        for(let i = 0; i < 3; i+=2){
          const card_img = document.createElement('img');
          card_img.src = 'cards_pic/'+ hand[0+i] + hand[1+i] + '.PNG';
          hand_div.appendChild(card_img);
        }
        hands_container.appendChild(hand_div);
      });
      document.body.appendChild(hands_container);
      console.log('----------');
    }

    //當鼠標懸浮到點上時顯示手牌
    function showPR(pr,amt){
      const pr_element = document.createElement("div");
      pr_element.className = 'pr_font'
      pr_element.innerHTML = 'PR值:' + pr + '手牌數:' + amt;
      pr_element.style.top = 0 + "px";
      chart.appendChild(pr_element)
    }
    
    //刪除點內容
    function removeElement(){
      try{
        const element1 = document.querySelector('.hands_container');
        element1.remove();
        const element2 = document.querySelector('.pr_font');
        element2.remove();
      }catch(e){
        console.log(e);
      }
    }
});